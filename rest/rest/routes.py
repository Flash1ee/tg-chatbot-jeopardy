from aiohttp import web

from rest.views import QuestionCRUD


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/api/question/{question:\d+}", QuestionCRUD)
