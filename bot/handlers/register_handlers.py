from bot.handlers.game_init import stop_game
from aiogram import Dispatcher
from aiogram import types


async def register_handlers_session(dp: Dispatcher):
    from bot.handlers.game_init import (
        game_end,
        game_status,
        session_start,
        show_themes,
        question_choose,
        answer,
        bot_action,
    )

    dp.register_message_handler(game_status, commands="status")
    dp.register_message_handler(session_start, commands="start_game")
    dp.register_message_handler(show_themes, commands="themes")
    dp.register_message_handler(game_end, commands="end")
    dp.register_message_handler(answer, commands="answer")
    dp.register_message_handler(stop_game, commands="stop")
    dp.register_message_handler(bot_action, content_types=[types.ContentType.TEXT])
    dp.register_callback_query_handler(question_choose)
