from datetime import datetime

from aiohttp import web
from aiohttp_apispec import request_schema, docs, response_schema, headers_schema

from app.base.responses import json_response
from app.base.schemas import BaseResponseSchema
from app.schemas import *

from app.game import models

QuestionParametrDocs = {
    "in": "path",
    "name": "question",
    "schema": {"type": "integer", "format": "int32"},
    "required": "true",
    "description": "Id of the question",
}


class QuestionCA(web.View):
    @docs(
        tags=["Question"],
        summary="Create question",
    )
    @headers_schema(BearerAuth)
    @request_schema(CreateQuestionRequestSchema)
    @response_schema(
        BaseResponseSchema, 200, description="New question has been created"
    )
    async def post(self):
        question: models.Question = await models.Question.create(
            content=self.request["data"]["content"],
            correct_answer=self.request["data"]["correct_answer"],
            score=self.request["data"]["score"],
            theme_id=self.request["data"]["theme_id"],
        )
        return json_response(data=QuestionResponseSchema().dump(question))

    @docs(
        tags=["Question"],
        summary="Get all questions",
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Questions was found")
    async def get(self):
        questions: models.Question = await models.Question.query.gino.all()
        return json_response(data=QuestionResponseSchema().dump(questions, many=True))


class QuestionRUD(web.View):
    @docs(
        tags=["Question"],
        summary="Get question",
        parameters=[QuestionParametrDocs],
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Question was found")
    async def get(self):
        question_id: int = int(self.request.match_info["question"])
        question = await models.Question.get(question_id)
        if not question:
            raise web.HTTPNotFound()
        return json_response(data=QuestionResponseSchema().dump(question))

    @docs(
        tags=["Question"],
        summary="Update question",
        parameters=[QuestionParametrDocs],
    )
    @headers_schema(BearerAuth)
    @request_schema(CreateQuestionRequestSchema)
    @response_schema(BaseResponseSchema, 200, description="Question was updated")
    async def patch(self):
        question_id: int = int(self.request.match_info["question"])
        question = await models.Question.get(question_id)
        if not question:
            raise web.HTTPNotFound()

        data = self.request["data"]
        await question.update(
            content=data["content"],
            correct_answer=data["correct_answer"],
            score=data["score"],
            theme_id=data["theme_id"],
        ).apply()

        return json_response(data=QuestionResponseSchema().dump(question))

    @docs(
        tags=["Question"],
        summary="Delete question",
        parameters=[QuestionParametrDocs],
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Question was deleted")
    async def delete(self):
        question_id: int = int(self.request.match_info["question"])
        question = await models.Question.get(question_id)
        if not question:
            raise web.HTTPNotFound()
        await question.delete()

        return json_response(data=None)


ThemeParametrDocs = {
    "in": "path",
    "name": "theme",
    "schema": {"type": "integer", "format": "int32"},
    "required": "true",
    "description": "Id of the theme",
}


class ThemeCA(web.View):
    @docs(
        tags=["Theme"],
        summary="Create theme",
    )
    @headers_schema(BearerAuth)
    @request_schema(CreateThemeRequestSchema)
    @response_schema(BaseResponseSchema, 200, description="New theme has been created")
    async def post(self):
        theme = await models.Theme.create(title=self.request["data"]["title"])
        return json_response(data=ThemeResponseSchema().dump(theme))

    @docs(
        tags=["Theme"],
        summary="Get all themes",
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Themes was found")
    async def get(self):
        themes = await models.Theme.query.gino.all()
        return json_response(data=ThemeResponseSchema().dump(themes, many=True))


class ThemeRUD(web.View):
    @docs(
        tags=["Theme"],
        summary="Get themes",
        parameters=[ThemeParametrDocs],
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Theme was found")
    async def get(self):
        theme_id: int = int(self.request.match_info["theme"])
        theme = await models.Theme.get(theme_id)
        if not theme:
            raise web.HTTPNotFound()
        return json_response(data=ThemeResponseSchema().dump(theme))

    @docs(
        tags=["Theme"],
        summary="Update theme",
        parameters=[ThemeParametrDocs],
    )
    @headers_schema(BearerAuth)
    @request_schema(CreateThemeRequestSchema)
    @response_schema(BaseResponseSchema, 200, description="Theme was updated")
    async def patch(self):
        theme_id: int = int(self.request.match_info["theme"])
        theme: models.Theme = await models.Theme.get(theme_id)
        if not theme:
            raise web.HTTPNotFound()
        await theme.update(title=self.request["data"]["title"]).apply()

        return json_response(data=ThemeResponseSchema().dump(theme))

    @docs(
        tags=["Theme"],
        summary="Delete theme",
        parameters=[ThemeParametrDocs],
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Theme was deleted")
    async def delete(self):
        theme_id: int = int(self.request.match_info["theme"])
        theme: models.Theme = await models.Theme.get(theme_id)
        if not theme:
            raise web.HTTPNotFound()

        await theme.delete()
        return json_response(data=None)


class QuestionsTheme(web.View):
    @docs(
        tags=["Question", "Theme"],
        summary="Get all questions in theme",
    )
    @headers_schema(BearerAuth)
    @response_schema(BaseResponseSchema, 200, description="Questions was found")
    async def get(self):
        theme_id: int = int(self.request.match_info["theme"])
        questions = await models.Question.query.where(
            models.Question.theme_id == theme_id
        ).gino.all()
        return json_response(data=QuestionResponseSchema().dump(questions, many=True))
