from bot.app.store.database.accessor import PostgresAccessor
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.bot.config import TOKEN
from bot.bot.handlers.register_handlers import register_handlers_session


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    # Объект бота
    # Диспетчер для бота
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.WARNING)

    pg = PostgresAccessor()
    await pg.create_session()
    await pg.db.gino.create_all()

    await register_handlers_session(dp)

    await dp.start_polling()

    await pg.stop_session()


if __name__ == "__main__":
    # Запуск бота
    from bot.bot.middlewares.user import UserMiddleware

    dp.middleware.setup(UserMiddleware())
    asyncio.run(main())
