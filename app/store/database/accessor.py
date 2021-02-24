class PostgresAccessor:
    def __init__(self) -> None:
        # from app.game import models

        # self.models = models
        self.db = None

    async def create_session(self) -> None:
        from app.store.database.models import db

        await db.set_bind(
            "postgresql://postgres:1234@localhost/postgres"
        )
        self.db = db
        # self.conn = await engine.acquire()

    async def stop_session(self) -> None:
        if self.db is not None:
            # await self.conn.release()
            await self.db.pop_bind().close()
