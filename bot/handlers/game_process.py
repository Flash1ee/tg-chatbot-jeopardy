from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class GameState(StatesGroup):
    round_generate = State()
    round_game = State()
    choice_question = State()
    answer_question = State()
    round_end = State()
