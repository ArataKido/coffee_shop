from collections.abc import Callable

from fastapi import HTTPException

from app.exceptions.application_exceptions import NotFoundException


from .handlers import handle_http_exception, handle_http_status_error, handle_network_error, handle_timeout_error

# from .invalid_distance import InvalidDistanceException
# from .venue_not_found import VenueNotFoundException

defined_exceptions: dict[Exception, Callable] = {
    NotFoundException: handle_http_exception,
    # VenueNotFoundException: handle_http_exception,
    HTTPException: handle_http_exception,
    # HTTPStatusError: handle_http_status_error,
    # NetworkError: handle_network_error,
    # TimeoutException: handle_timeout_error,
}
