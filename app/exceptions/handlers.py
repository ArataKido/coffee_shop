from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

# from httpx import HTTPStatusError, NetworkError, TimeoutException


async def handle_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code or 500,
        content={"detail": exc.detail or "Internal Server Error"},
    )


# async def handle_http_status_error(request: Request, exc: HTTPStatusError):
#     return JSONResponse(
#         status_code=exc.response.status_code or 500,
#         content={"detail": exc.response.json() or "Internal Server Error"},
#     )

# async def handle_timeout_error(request: Request, exc: TimeoutException):
#     return JSONResponse(
#         status_code=504,
#         content={"detail": "Connection timed out"},
#     )

# async def handle_network_error(request: Request, exc: NetworkError):
#     return JSONResponse(
#         status_code=503,
#         content={"detail": "Failed to establish connection"},
#     )
