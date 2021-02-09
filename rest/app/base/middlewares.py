from aiohttp import web

from app.base.responses import json_response, error_json_response

import traceback
import sys


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except web.HTTPException as ex:
        return json_response(status=ex.status, text_status=ex.text, data={})
    except Exception as e:
        t = traceback.format_exc()
        return json_response(status=500, text_status=str(e), data=t.split("\n"))


@web.middleware
async def auth_middleware(request, handler):
    if request.path.startswith("/api") and not ('Authorization' in request.headers.keys() and
            request.headers['Authorization'] != 'Bearer ' + request.app.config["auth"]["token"]):
        return error_json_response(status=401, text_status="Unauthorized", message="Unauthorized")

    return await handler(request)
