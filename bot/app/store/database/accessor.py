from bot.bot.config import cfg

class PostgresAccessor:
    def __init__(self) -> None:
        from bot.app.game import models

        self.models = models
        self.db = None

    async def create_session(self) -> None:
        from bot.app.store.database.models import db

        await db.set_bind(cfg["postgres"]["url"])
        self.db = db
        # self.conn = await engine.acquire()

    async def stop_session(self) -> None:
        if self.db is not None:
            # await self.conn.release()
            await self.db.pop_bind().close()
