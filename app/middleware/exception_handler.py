from exceptions import defined_exceptions
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def setup_custom_exception_handlers(app: FastAPI):
    for exc_type, handler in defined_exceptions.items():

        async def create_handler(request, exc, h=handler):
            return await h(request, exc)

        app.add_exception_handler(exc_type, create_handler)


async def handle_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"detail": "Service unavailable"},
        )
