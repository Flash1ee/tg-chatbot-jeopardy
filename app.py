from bot.middlewares.user import UserMiddleware
import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.config import TOKEN
from bot.keyboard import get_keyboard
from bot.handlers.register_handlers import register_handlers_session

from bot.middlewares.db import PostgressMiddleware


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    # Объект бота
    # Диспетчер для бота
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    await register_handlers_session(dp)

    await dp.start_polling()


if __name__ == "__main__":
    # Запуск бота
    dp.middleware.setup(PostgressMiddleware())
    dp.middleware.setup(UserMiddleware())
    asyncio.run(main())
