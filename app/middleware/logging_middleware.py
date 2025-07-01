from json.decoder import JSONDecodeError
import time

from anyio import WouldBlock
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import Config
from app.dependencies.providers.service_provider import ServiceProvider


config = Config()
logger = ServiceProvider().get_logger(config)


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
            req_body_bytes = await request.body()  # Read the raw body bytes

            # Save the body for logging
            req_body = None
            content_type = request.headers.get("content-type", "")
            if request.method in ("POST", "PUT", "PATCH"):
                if "application/x-www-form-urlencoded" in content_type:
                    from starlette.datastructures import FormData
                    from urllib.parse import parse_qs
                    parsed = parse_qs(req_body_bytes.decode())
                    req_body = dict((k, v[0] if len(v) == 1 else v) for k, v in parsed.items())
                elif "application/json" in content_type:
                    import json

                    try:
                        req_body = json.loads(req_body_bytes)
                    except Exception:
                        req_body = None

            # Patch the request stream so downstream can read it again
            async def receive():
                return {"type": "http.request", "body": req_body_bytes, "more_body": False}

            request._receive = receive

            response = await call_next(request)
            res_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(res_body))
            res_body_bytes = b"".join(res_body)
            try:
                res_body_str = res_body_bytes.decode()
            except Exception:
                res_body_str = str(res_body_bytes)
            task = BackgroundTask(log_request_response, request, response, res_body_str, req_body, start_time)

            return Response(
                content=res_body_str,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
                background=task,
            )
        except WouldBlock as e:
            logger.error(f"WouldBlock error encountered: {e!s}")  # noqa: TRY400
            return Response(content="Service temporarily unavailable.", status_code=503)
        except JSONDecodeError as e:
            process_time = time.time() - start_time
            logger.error(f"Error during request - Time taken: {process_time:.4f}s")  # noqa: TRY400
            logger.error(f"Request json is empty. Details: {e!s}")  # noqa: TRY400
            raise
        except Exception as e:
            process_time = time.time() - start_time

            logger.error(f"Error during request - Time taken: {process_time:.4f}s")  # noqa: TRY400
            logger.error(f"Error details: {e}")  # noqa: TRY400
            logger.error("-------------------------")  # noqa: TRY400
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
