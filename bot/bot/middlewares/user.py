from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.message import Message
from aiogram import types


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message: Message, data):
        from bot.bot.helpers.gameHelper import GameHelper

        await GameHelper.registerUser(message.from_user.id)
