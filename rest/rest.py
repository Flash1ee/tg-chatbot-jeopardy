import asyncio
import logging

from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware

from app.base.middlewares import error_middleware
from app.settings import config, BASE_DIR

from app.store.database.accessors import PostgresAccessor

from app.routes import setup_routes as setup_game_routes

database_accessor = PostgresAccessor()

asyncio.get_event_loop().run_until_complete(
    database_accessor.check_connection_and_create_tables()
)


def setup_external_libraries(app: web.Application) -> None:
    setup_aiohttp_apispec(
        app=app,
        title="Documentation",
        version="v1",
        url="/swagger.json",
        swagger_path="/swagger",
    )


def setup_config(app: web.Application) -> None:
    app.config = config
    app["config"] = config


def setup_routes(app: web.Application) -> None:
    setup_game_routes(app)


def setup_accessors(app: web.Application) -> None:
    database_accessor.setup(app)
    pass


def setup_middlewares(app: web.Application) -> None:
    app.middlewares.append(error_middleware)
    app.middlewares.append(validation_middleware)


def setup_logging(_: web.Application) -> None:
    logging.basicConfig(level=logging.INFO)


def setup_app(app: web.Application) -> None:
    setup_config(app)
    setup_routes(app)
    setup_accessors(app)
    setup_external_libraries(app)
    setup_middlewares(app)
    setup_logging(app)


app = web.Application()

if __name__ == "__main__":
    setup_app(app)
    web.run_app(app, port=config["web"]["port"])
