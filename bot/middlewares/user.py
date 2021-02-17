from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types.message import Message
from bot.helpers.gameHelper import GameHelper
from aiogram import types


class UserMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_pre_process_message(self, message: Message, data):
        await GameHelper.registerUser(message.from_user.id)
