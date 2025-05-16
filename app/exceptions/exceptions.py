from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Looking object was not found."):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail
