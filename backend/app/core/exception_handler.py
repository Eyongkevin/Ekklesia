from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions.base import AppException

async def app_exception_handler(
    request: Request,
    exc: Exception
):
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content = {
                "error": {
                    "type": exc.__class__.__name__,
                    "detail": exc.detail
                }
            }
        )
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "INTERNAL_SERVER_ERROR",
                "detail": "Internal server error"
            }
        }
    )
