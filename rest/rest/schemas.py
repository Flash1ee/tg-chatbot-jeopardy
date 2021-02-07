import datetime

from marshmallow import Schema, fields

from rest.base.schemas import BaseResponseSchema


class Question(Schema):
    id: int = fields.Integer()
    content: str = fields.String()
    correct_answer: str = fields.String()
    score: int = fields.Integer()
    theme_id: int = fields.Integer()

class QuestionResponseSchema(BaseResponseSchema):
    question = fields.Nested(Question)

class ListQuestionResponseSchema(BaseResponseSchema):
    questions = fields.Nested(Question, many=True)

class CreateQuestionRequestSchema(Schema):
    content: str = fields.String()
    correct_answer: str = fields.String()
    score: int = fields.Integer()
    theme_id: int = fields.Integer()

class PatchQuestionRequestSchema(Schema):
    content: str = fields.String(required=False)
    correct_answer: str = fields.String(required=False)
    score: int = fields.Integer(required=False)
    theme_id: int = fields.Integer(required=False)

class GetQuestionRequestSchema(Schema):
    pass



