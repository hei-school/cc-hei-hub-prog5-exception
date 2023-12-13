import logging
import traceback
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from utils import parse_error_message, app, separation_message_type


error_status_codes = [400, 402, 403, 501]


# CUSTOM EXCEPTIONS


@app.middleware("http")
async def set_timeout(request: Request, call_next):
    response = await call_next(request)
    response.timeout = 5  # seconds
    return response


def cast_message_to_exception_message(error_type, message):
    return f"{error_type}{separation_message_type}{message}"


def raise_exception(code, type, message):
    msg_error = cast_message_to_exception_message(type, message)
    return HTTPException(status_code=code, detail=msg_error)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    error_trace = traceback.format_exc()
    logging.error(error_trace)
    logging.error(" --- --- --- --- --- --- --- --- ---" + "\n" + "\n")
    error_message = parse_error_message(exc)
    return JSONResponse(status_code=exc.status_code, content=error_message)


for status_code in error_status_codes:

    @app.exception_handler(status_code)
    async def specific_exception_handler(request, exc):
        error_message = parse_error_message(exc)
        return JSONResponse(status_code=exc.status_code, content=error_message)
