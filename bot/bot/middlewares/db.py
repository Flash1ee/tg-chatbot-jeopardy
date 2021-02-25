from aiogram.dispatcher.middlewares import BaseMiddleware
from app.store.database.accessor import PostgresAccessor
from aiogram import types


class PostgressMiddleware(BaseMiddleware):
    def __init__(self):
        self.postgress = PostgresAccessor()
        super(PostgressMiddleware, self).__init__()

    async def on_pre_process_message(self, *args):
        await self.postgress.create_session()
        await self.postgress.db.gino.create_all()

    async def on_post_process_message(self, *args):
        await self.postgress.stop_session()
