from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from aiogram import types, Dispatcher

'''
Кнопка с вопросом имеет вид "{theme_num}_{question_num}_question"
theme_num - [0:5]
question_num - [0:4]
Нужна для обработки вопроса
Игнорируем выбор кнопки с темой
Кнопка с темой имеет вид "{theme_num}_theme"
'''
async def get_keyboard(round_tasks: dict):
    # Генерация клавиатуры.
    buttons = []
    theme_num = 0
    question_num = 0
    for key, value in round_tasks.items():
        question_num = 0
        buttons.append(types.InlineKeyboardButton(
            text=key, callback_data=f"{theme_num}_theme"))
        for data in value:
            price = data["price"]
            question = data["question"]
            if question == "":
                buttons.append(types.InlineKeyboardButton(
                    text="", callback_data="empty"))
            else:
                buttons.append(types.InlineKeyboardButton(
                    text=price, callback_data=f"{theme_num}_{question_num}_question"))
            question_num += 1
        theme_num += 1

    keyboard = types.InlineKeyboardMarkup(row_width=question_num + 1)
    keyboard.add(*buttons)
    return keyboard
