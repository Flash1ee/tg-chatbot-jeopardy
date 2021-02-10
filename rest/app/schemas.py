import datetime

from marshmallow import Schema, fields, ValidationError

from app.base.schemas import BaseResponseSchema
from app.settings import config
from aiohttp import web


def validate_bearer(header: str):
    if header != "Bearer " + config["auth"]["token"]:
        raise web.HTTPForbidden()


class BearerAuth(Schema):
    Authorization = fields.Str(validate=validate_bearer, required=True)


class QuestionResponseSchema(Schema):
    id: int = fields.Integer()
    content: str = fields.String()
    correct_answer: str = fields.String()
    score: int = fields.Integer()
    theme_id: int = fields.Integer()


class CreateQuestionRequestSchema(Schema):
    content: str = fields.String()
    correct_answer: str = fields.String()
    score: int = fields.Integer()
    theme_id: int = fields.Integer()


class ThemeResponseSchema(BaseResponseSchema):
    id: int = fields.Integer()
    title: str = fields.String()


class CreateThemeRequestSchema(Schema):
    title: str = fields.String()
