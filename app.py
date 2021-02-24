import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config import TOKEN
from bot.handlers.register_handlers import register_handlers_session



bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    # Объект бота
    # Диспетчер для бота
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.WARNING)

    await register_handlers_session(dp)

    await dp.start_polling()


if __name__ == "__main__":
    # Запуск бота
    from bot.middlewares.user import UserMiddleware
    from bot.middlewares.db import PostgressMiddleware

    dp.middleware.setup(PostgressMiddleware())
    dp.middleware.setup(UserMiddleware())
    asyncio.run(main())
