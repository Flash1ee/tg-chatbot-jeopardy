from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class WaitState(StatesGroup):
    session_start = State()
    session_active = State()

# /start_game
async def game_start(message: types.Message):
    await message.answer("Игра начинается")
    await WaitState.session_active.set()

async def game_end(message: types.Message,  state: FSMContext):
    await state.finish()
    await message.answer("Игра завершена. Спасибо за участие")
    await message.answer("Статистику украли цыгане", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_session(dp: Dispatcher):
    dp.register_message_handler(game_start, commands="start", state = "*")
    dp.register_message_handler(game_end, commands="end", state=WaitState.session_active)