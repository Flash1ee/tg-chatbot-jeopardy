from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from aiogram import types, Dispatcher


def get_keyboard(round_tasks: dict):
    # Генерация клавиатуры.
    buttons = []
    theme_num = 0
    question_num = 0
    for key, value in round_tasks:
        question_num = 0
        buttons.append(types.InlineKeyboardButton(
            text=key, callback_data="{theme_num}_theme"))
        for question in value:
            if question == "":
                buttons.append(types.InlineKeyboardButton(
                    text="", callback_data="empty"))
            else:
                buttons.append(types.InlineKeyboardButton(
                    text=question, callback_data="{theme_num}_{question_num}_question"))
            question_num += 1
        theme_num += 1

    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=question_num + 1)
    keyboard.add(*buttons)
    return keyboard
