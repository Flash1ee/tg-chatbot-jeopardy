from aiogram import types
from bot.helpers.gameHelper import GameHelper, GameState
from app.store.database.models import db
import app.game.models as m
import bot.keyboard as kb
import asyncio


async def bg_task(s, func, *args):
    await asyncio.sleep(s)
    await func(*args)


# async def load_timers(db):
#     sessions: List[m.Session] = await (m.Session.query.select_from(
#         m.Session.join(
#             m.Round, m.Round.session_id == m.Session.id
#         )
#     )
#         .select_from(
#         m.Round.join(
#             m.RoundQuestion, m.RoundQuestion.round_id == m.Round.id
#         )
#     )
#         .where(m.RoundQuestion.status == m.RoundQuestionStatus.answered.active)
#         .gino.all()
#     )

#     for session in sessions:
#         game = GameHelper(session.chat_id)
#         await game.getQuestion()
#         (datetime.now() - game.rq.created_at).seconds

#         asyncio.create_task(bg_task(game.time_to_answer.seconds,
#                                     check_timeout_answer, call=None, game=game))


async def game_status(message: types.Message):
    game = GameHelper(message.chat.id, db)
    state = await game.GetState()
    if state != GameState.not_active:
        if state == GameState.active:
            ans = "Ваша сессия активна"
        elif state == GameState.wait_answer:
            ans = "Ожидается ответ на вопрос"
        elif state == GameState.wait_question:
            ans = "Ожидается выбор вопроса"
        else:
            ans = "Что-то поломалось " + str(state)
        await message.answer(ans)
    else:
        await message.answer("Игра не активна")


async def session_start(message: types.Message):
    await message.answer("Создаем сессию")
    game = GameHelper(message.chat.id, db)
    state = await game.GetState()
    if state != GameState.not_active:
        await message.answer("Вы уже играете")
        return
    await game.createSession()
    await game.startRound()
    await show_themes(message)


async def stats(message: types.Message):
    game = GameHelper(message.chat.id, db)

    state = await game.GetState()
    if state == GameState.not_active:
        await message.answer("А вы не играете)")
        return

    scores = await game.getScores()

    score_users = [
        (
            score,
            await message.bot.get_chat_member(
                chat_id=message.chat.id, user_id=score.user_id
            ),
        )
        for score in scores
    ]

    leaders = "\n".join(
        [
            "{:} - {:}".format(user.user.full_name, score.score)
            for score, user in score_users
        ]
    )

    await message.answer("Таблица рейтинга: \n" + leaders)

    pass


async def show_themes(message: types.Message):
    game = GameHelper(message.chat.id, db)
    state = await game.GetState()
    if state != GameState.wait_question:
        await message.answer("Нельзя")
        return
    table = await game.table()

    have_question = 0
    for key, value in table.items():
        for price, is_used in value["answers"].items():
            if not is_used:
                have_question += 1
    if not have_question:
        round = await game.startRound()
        if not round:
            await message.answer("Игра окончена!")
        else:
            await message.answer("Начинаем новый раунд")
            await show_themes(message)
        return
    my_kb = await kb.get_keyboard(table)

    mes = "Раунд №" + str(game.round.number) + "\n"

    user_id = await game.choosingUser()
    user = None
    if user_id:
        user = await message.bot.get_chat_member(
            chat_id=message.chat.id, user_id=user_id
        )
        mes += "Отвечает " + user.user.mention + "\n"
    mes += "\n Выберите тему\n"
    await message.answer(mes, reply_markup=my_kb)

    if not user:
        return

    asyncio.create_task(
        bg_task(
            game.time_to_choose.seconds,
            check_timeout_choose,
            message,
            game,
            user,
            game.last_rq.id,
        )
    )


async def check_timeout_choose(message, game, user, last_rq_id):
    await game.update_data()
    await game.getLastQuestion()

    if (
        await game.GetState() == GameState.wait_question
        and game.last_rq.id == last_rq_id
    ):
        await message.answer(
            user.user.mention + ", время вышло. Теперь любой выбирает тему."
        )


async def game_end(message: types.Message):
    game = GameHelper(chat_id=message.chat.id, db=db)
    print(await game.GetSession())
    await message.answer("Игра завершена. Спасибо за участие")
    await message.answer(
        "Статистику украли цыгане", reply_markup=types.ReplyKeyboardRemove()
    )


async def question_choose(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    game = GameHelper(chat_id)

    action = call.data.split("_")

    if len(action) != 3:
        await call.answer("Выберите доступный вопрос")
        return

    user_id = await game.choosingUser()

    if user_id and user_id != call.from_user.id:
        await call.answer("Не ваша очередь отвечать")
        return

    await call.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=call.message.message_id,
        inline_message_id=call.inline_message_id,
        reply_markup=None,
    )

    theme_id, score = int(action[0]), int(action[1])

    mes = "Вопрос №" + str(theme_id) + "-" + str(score) + "\n"

    question, rq = await game.createRoundQuestion(score=score, theme_id=theme_id)

    mes += "Вопрос :" + question.content + "\n"
    mes += "Ответ :" + question.correct_answer + "\n"

    await call.bot.send_message(chat_id=chat_id, text=mes)

    asyncio.create_task(
        bg_task(game.time_to_answer.seconds, check_timeout_answer, call, game)
    )


async def check_timeout_answer(call, game):
    rq_id = game.rq.id
    game.db = db

    await game.update_data()

    if await game.GetState() == GameState.wait_answer and game.rq.id == rq_id:
        await call.bot.send_message(
            chat_id=game.chat_id,
            text="Время вышло. Никто не ответил на вопрос правильно.",
        )
        await game.stopQuestion()
        await show_themes(call.message)


async def answer(message: types.Message):
    game = GameHelper(message.chat.id, db=db)

    q, qr = await game.getQuestion()

    user_answer = message.text.replace("/answer", "")
    answer = await game.answerQuestion(answer=user_answer, user_id=message.from_user.id)

    await message.answer(answer.status, reply=True)

    if answer.status == m.AnswerStatus.correct:
        await show_themes(message)


async def stop_game(message: types.Message):
    game = GameHelper(message.chat.id, db=db)

    state = await game.GetState()
    if state != GameState.not_active:
        await game.stop()
        await message.answer("Игра остановлена", reply=True)
    else:
        await message.answer("Вы не играете", reply=True)


async def bot_action(message: types.Message):
    game = GameHelper(message.chat.id, db=db)
    state = await game.GetState()
    if state == GameState.wait_answer:
        await answer(message)
    elif state == GameState.wait_question:
        await message.answer("Выберите вопрос в таблице", reply=True)
    elif state == GameState.not_active:
        await message.answer("Чтобы начать игру введите /start_game", reply=True)
