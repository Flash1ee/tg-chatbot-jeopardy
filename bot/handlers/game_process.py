from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.handlers.wait import WaitState, game_start
from bot.config import data

chosing_user_id = 0
class GameState(StatesGroup):
    round_generate = State()
    round_game = State()
    choice_question = State()
    answer_question = State()
    round_end = State()

async def round_init(message: types.Message,  state: FSMContext):
    await GameState.round_game.set()
    await message.answer("Генерируем раунд N")
    choosing_user = message.chat.first_name
    game_start(message, choosing_user, data)
    # await message.answer("Статистику украли цыгане", reply_markup=types.ReplyKeyboardRemove())

