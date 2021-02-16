from aiogram import Dispatcher


async def register_handlers_session(dp: Dispatcher):
    from bot.handlers.game_init import game_end, game_start
    dp.register_message_handler(game_start, commands="start")
    dp.register_message_handler(game_end, commands="end")
