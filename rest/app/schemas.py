import datetime

from marshmallow import Schema, fields

from app.base.schemas import BaseResponseSchema


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