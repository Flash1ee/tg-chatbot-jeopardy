from aiohttp import web

from app.views import QuestionCA, QuestionRUD, ThemeCA, ThemeRUD, QuestionsTheme


def setup_routes(app: web.Application) -> None:
    app.router.add_view("/api/question/{question:\d+}", QuestionRUD)
    app.router.add_view("/api/question", QuestionCA)

    app.router.add_view("/api/theme/{theme:\d+}", ThemeRUD)
    app.router.add_view("/api/theme/{theme:\d+}/questions", QuestionsTheme)
    app.router.add_view("/api/theme", ThemeCA)
