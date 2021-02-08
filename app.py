"""Сборка всего приложения."""
import logging

from vkbottle.bot import Bot, Message
from vkbottle.tools.dev_tools.loop_wrapper import LoopWrapper

from bot.blueprints import bps
# from src.config import BOT_TOKEN
# from src.initialize import setup_db
# from src.middlewares.no_bot_middleware import NoBotMiddleware
from bot.config import TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def init_bot():
    """Фабрика для бота."""
    bot_ = Bot(token=TOKEN)
    setup_middlewares(bot_)
    setup_blueprints(bot_)

    return bot_


def setup_blueprints(bot_: Bot):
    """Инициализация blueprints."""
    for bp in bps:
        bp.load(bot_)


def setup_middlewares(bot_: Bot):
    """Инициализация middlewares."""
    # bot_.labeler.message_view.register_middleware(NoBotMiddleware())


bot = init_bot()



