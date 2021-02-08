import ssl

from aiohttp import web
from sqlalchemy import func


class PostgresAccessor:
    def __init__(self) -> None:
        from app.game import models

        self.models = models
        self.db = None

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, app: web.Application):
        from app.store.database.models import db

        self.config = app.config["postgres"]
        if self.config["ssl"]:
            ctx = ssl.create_default_context(cafile="")
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            await db.set_bind(self.config["url"], ssl=ctx)
        else:
            await db.set_bind(self.config["url"])
        self.db = db
        app.db = self

    async def _on_disconnect(self, _) -> None:
        if self.db is not None:
            await self.db.pop_bind().close()