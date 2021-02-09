import datetime

from marshmallow import Schema, fields, ValidationError

from app.base.schemas import BaseResponseSchema
from app.settings import config


def validate_bearer(header: str):
    print(header, config["auth"]["token"])

    if header != 'Bearer ' + config["auth"]["token"]:
        raise ValidationError("Unauthorized")
        # return error_json_response(status = 401, text_status = "Unauthorized", message = "Unauthorized")

class BearerAuth(Schema):
  Authorization=fields.Str(validate = validate_bearer)

class QuestionResponseSchema(Schema):
    id: int=fields.Integer()
    content: str=fields.String()
    correct_answer: str=fields.String()
    score: int=fields.Integer()
    theme_id: int=fields.Integer()

class CreateQuestionRequestSchema(Schema):
    content: str=fields.String()
    correct_answer: str=fields.String()
    score: int=fields.Integer()
    theme_id: int=fields.Integer()

class ThemeResponseSchema(BaseResponseSchema):
    id: int=fields.Integer()
    title: str=fields.String()

class CreateThemeRequestSchema(Schema):
    title: str=fields.String()
