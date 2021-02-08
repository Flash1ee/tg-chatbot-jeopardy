from vkbottle.bot import Blueprint, Message

bp = Blueprint(name = "hello")

@bp.on.chat_message()
async def hello_handler(message: Message):
    await message.answer("Добро пожаловать в Свою игру")
