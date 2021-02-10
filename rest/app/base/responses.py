from aiohttp import web


def json_response(
    status: int = 200, text_status: str = "ok", data: dict = None
) -> web.Response:
    return web.json_response(status=status, data={"data": data, "status": text_status})


def error_json_response(
    status: int = 400,
    text_status: str = "Bad request",
    message: str = "",
    data: dict = {},
) -> web.Response:
    if not message and text_status:
        message = text_status

    return web.json_response(
        status=status, data={"data": data, "status": text_status, "message": message}
    )
