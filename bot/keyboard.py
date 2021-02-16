from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import MessageNotModified
from aiogram.utils.callback_data import CallbackData
from aiogram import types, Dispatcher

"""
Некрасивый пример клавиатуры для вопросов
#todo переделать под бд
"""


async def get_keyboard(round_tasks: dict):
    # Генерация клавиатуры.

    keyboard = types.InlineKeyboardMarkup()

    for key, value in round_tasks.items():
        keyboard.row(
            types.InlineKeyboardButton(
                text=value["title"], callback_data=f"{key}_theme"
            )
        )

        buttons = []
        for price, is_used in value["answers"].items():
            if is_used:
                buttons.append(
                    types.InlineKeyboardButton(text="-", callback_data="empty")
                )
            else:
                buttons.append(
                    types.InlineKeyboardButton(
                        text=str(price), callback_data=f"{key}_{price}_question"
                    )
                )
        keyboard.row(*buttons)

    return keyboard
