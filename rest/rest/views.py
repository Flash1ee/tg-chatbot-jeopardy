from datetime import datetime

from aiohttp import web
from aiohttp_apispec import request_schema, docs, response_schema

from rest.base.responses import json_response
from rest.base.schemas import BaseResponseSchema
from rest.schemas import CreateQuestionRequestSchema, QuestionResponseSchema, GetQuestionRequestSchema, PatchQuestionRequestSchema


QuestionParametrDocs = {
    'in': 'path',
    'name': 'question',
    'schema': {'type': 'integer', 'format':	'int32'},
    'required': 'true',
    'description': "Id of the question",
}


class QuestionCRUD(web.View):
    @docs(
        tags=["Question"],
        summary="Get question",
        parameters=[QuestionParametrDocs],

    )
    @request_schema(GetQuestionRequestSchema)
    @response_schema(BaseResponseSchema, 200,
                     description="Question was found")
    async def get(self):
        message = {
            "id": 1,
            "content": "Simple",
            "correct_answer": "Hard",
            "score": 1,
            "theme_id": 1,
        }
        return json_response(data=message)

    @docs(
        tags=["Question"],
        summary="Create question",
        parameters=[QuestionParametrDocs],
    )
    @request_schema(CreateQuestionRequestSchema)
    @response_schema(BaseResponseSchema, 200,
                     description="New question has been created")
    async def post(self):
        return json_response(data=self.request["data"])

    @docs(
        tags=["Question"],
        summary="Update question",
        parameters=[QuestionParametrDocs],
    )
    @request_schema(PatchQuestionRequestSchema)
    @response_schema(BaseResponseSchema, 200,
                     description="Question was updated")
    async def patch(self):
        message = {
            "id": 1,
            "content": "Simple",
            "correct_answer": "Hard",
            "score": 1,
            "theme_id": 1,
        }
        return json_response(data=message)
    
    @docs(
        tags=["Question"],
        summary="Delete question",
        parameters=[QuestionParametrDocs],
    )
    @request_schema(GetQuestionRequestSchema)
    @response_schema(BaseResponseSchema, 200,
                     description="Question was deleted")
    async def delete(self):
        return json_response(data=None)