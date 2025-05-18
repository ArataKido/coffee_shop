import json
from json.decoder import JSONDecodeError
import time

from anyio import WouldBlock
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from app.utils.loggers.logger import Logger

logger = Logger()


def get_replay_receive(body_bytes: bytes):
    """Return an ASGI receive() that replays body_bytes once, then empties."""
    received = False

    async def receive():
        nonlocal received
        if not received:
            received = True
            # First call: real body
            return {"type": "http.request", "body": body_bytes, "more_body": False}
        # Subsequent calls: empty body to signal completion
        return {"type": "http.request", "body": b"", "more_body": False}

    return receive


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            req_body = await request.json() if request.method in ("POST", "PUT", "PATCH") else None
            response = await call_next(request)
            res_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(res_body))
            if res_body:
                res_body = res_body[0].decode()

            response.background = BackgroundTask(
                log_request_response, request, response, res_body, req_body, start_time
            )

            return response

        except WouldBlock as e:
            logger.error(f"WouldBlock error encountered: {e!s}")
            return Response(content="Service temporarily unavailable.", status_code=503)
        except JSONDecodeError as e:
            process_time = time.time() - start_time
            logger.error(f"Error during request - Time taken: {process_time:.4f}s")
            logger.error(f"Request json is empty. Details: {e!s}")
            raise

        except Exception as e:
            process_time = time.time() - start_time

            logger.error(f"Error during request - Time taken: {process_time:.4f}s")
            logger.error(f"Error details: {e}")
            logger.error("-------------------------")

            raise


async def log_request_response(request: Request, response, res_body, req_body, start_time: float):
    """Background task to log request and response details."""
    process_time = time.time() - start_time

    logger.info(f"Incoming request: {request.method} {request.url}")
    logger.info(f"Request headers: {dict(request.headers)}")

    if req_body:
        logger.info(f"Request body: {req_body}")

    logger.info(f"Request completed - Status: {response.status_code} - Time taken: {process_time:.4f}s")

    logger.info(f"Response headers: {dict(response.headers)}")
    if len(res_body) < 1000:  # Avoid logging large response bodies
        logger.info(f"Response body: {res_body}")
    else:
        logger.info("Response body too large to log")

    logger.info("-------------------------")
