import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot.handlers.wait import register_handlers_session
import bot.config as cfg

TOKEN = cfg.TOKEN

async def main():
    # Объект бота
    bot = Bot(token=TOKEN)
    # Диспетчер для бота
    dp = Dispatcher(bot, storage=MemoryStorage())
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)

    async def set_commands(bot: Bot):
        commands = [
            BotCommand(command="/start", description="Начать игру"),
            BotCommand(command="/end", description="Завершить игру"),
        ]
        await bot.set_my_commands(commands)

    # Хэндлер на команду /test1
    @dp.message_handler(commands="test1")
    async def cmd_test1(message: types.Message):
        await message.reply("Test 1")

    register_handlers_session(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == "__main__":
    # Запуск бота
    asyncio.run(main())