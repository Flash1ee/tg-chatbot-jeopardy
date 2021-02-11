from aiogram.types import BotCommand
from aiogram import Bot


async def set_commands(bot: Bot):
        commands = [
            BotCommand(command="/start", description="Начать игру"),
            BotCommand(command="/end", description="Завершить игру"),
        ]
        await bot.set_my_commands(commands)