from aiogram import Dispatcher, types
from aiogram.types import message
from bot.helpers.gameHelper import GameHelper, GameState
from app.store.database.models import db
import app.game.models as m
import bot.keyboard as kb

# /start_game


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
    if user_id:
        user = await message.bot.get_chat_member(
            chat_id=message.chat.id, user_id=user_id
        )
        mes += "Отвечает " + user.user.mention + "\n"
    mes += "\n Выберите тему\n"
    await message.answer(mes, reply_markup=my_kb)


async def game_end(message: types.Message):
    game = GameHelper(chat_id=message.chat.id, db=db)
    print(await game.GetSession())
    await message.answer("Игра завершена. Спасибо за участие")
    await message.answer(
        "Статистику украли цыгане", reply_markup=types.ReplyKeyboardRemove()
    )


async def question_choose(call: types.CallbackQuery):

    from app.store.database.accessor import PostgresAccessor

    pg = PostgresAccessor()
    await pg.create_session()

    chat_id = call.message.chat.id
    game = GameHelper(chat_id, db=pg.db)

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
    # question_time = 30
    mes += "Вопрос :" + question.content + "\n"
    mes += "Ответ :" + question.correct_answer + "\n"
    # mes += "На ответ " + question_time + "секунд\n"

    await call.bot.send_message(chat_id=chat_id, text=mes)

    await pg.stop_session()


async def answer(message: types.Message):
    game = GameHelper(message.chat.id, db=db)

    q, qr = await game.getQuestion()
    print(q.correct_answer)
    user_answer = message.text.replace("/answer", "")
    answer = await game.answerQuestion(answer=user_answer, user_id=message.from_user.id)

    await message.answer(answer.status, reply=True)

    if answer.status == m.AnswerStatus.correct:
        await show_themes(message)


async def bot_action(message: types.Message):
    game = GameHelper(message.chat.id, db=db)
    state = await game.GetState()
    if state == GameState.wait_answer:
        await answer(message)
    elif state == GameState.wait_question:
        await message.answer("Выберите вопрос в таблице", reply=True)
    elif state == GameState.not_active:
        await message.answer("Чтобы начать игру введите /start_game", reply=True)
