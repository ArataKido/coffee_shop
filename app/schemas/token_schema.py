from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    # refresh_token: str
    # expires_in: int
    # scope: str


class TokenData(BaseModel):
    user_id: int
