from anyio import WouldBlock
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask
import time
from app.utils.loggers.logger import Logger

logger = Logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        try:
            req_body = await request.json() if request.method in ("POST", "PUT", "PATCH") else None
            response = await call_next(request)
            # req_body_decoded = req_body.decode()

            # I had to do this here not in the background task because the response body would be consumed and gone
            res_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(res_body))
            res_body = res_body[0].decode()

            response.background = BackgroundTask(log_request_response, request, response, res_body, req_body, start_time)
            
            return response
        
        except WouldBlock as e:
            logger.error(f"WouldBlock error encountered: {str(e)}")
            return Response(content="Service temporarily unavailable.", status_code=503)
        
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
