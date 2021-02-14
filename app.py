import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers.wait import register_handlers_session
from bot.config import TOKEN, DATA
from bot.commands import set_commands
from bot.keyboard import get_keyboard


async def main():
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер для бота
    dp = Dispatcher(bot, storage=MemoryStorage())
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    register_handlers_session(dp)

    await set_commands(bot)
    await dp.start_polling()
    keyboard_handlers(dp)
    


if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())


def keyboard_handlers(dp: Dispatcher): 
    count_themes = 6
    count_questions = 5

    for i in range(count_themes):
        for j in range(count_questions):
            dp.callback_query_handler(text = f"{i}_{j}_question")
            async def send_question(call: types.CallbackQuery):
                await call.message.answer(text = "Ваш вопрос")
