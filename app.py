import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers.wait import register_handlers_session
import bot.config as cfg
from bot.commands import set_commands

TOKEN = cfg.TOKEN

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


if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())



