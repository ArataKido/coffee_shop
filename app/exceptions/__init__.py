from collections.abc import Callable

from fastapi import HTTPException

from app.exceptions.application_exceptions import NotFoundException


from .handlers import handle_http_exception

# from .invalid_distance import InvalidDistanceException
# from .venue_not_found import VenueNotFoundException

defined_exceptions: dict[Exception, Callable] = {
    NotFoundException: handle_http_exception,
    HTTPException: handle_http_exception,
}
