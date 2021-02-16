from aiogram import Dispatcher, types
from bot.helpers.gameHelper import GameHelper, GameState
from app.store.database.models import db

# /start_game

async def game_start(message: types.Message):
    await message.answer("Игра начинается")
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
            ans = "Что-то поломалось"
        await message.answer(ans)
    else:
        await message.answer("Ваша сессия зарегистирована")


async def game_end(message: types.Message):
    game = GameHelper(chat_id=message.chat.id, db=db)
    print(await game.GetSession())
    await message.answer("Игра завершена. Спасибо за участие")
    await message.answer("Статистику украли цыгане", reply_markup=types.ReplyKeyboardRemove())



