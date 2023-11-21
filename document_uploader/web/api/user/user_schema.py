from pydantic import BaseModel


class UserSignup(BaseModel):
    """
    User Signup Data.

    Schema for user registration data.
    """

    username: str
    password: str


class UserLogin(BaseModel):
    """
    User Login Data.

    Schema for user login data.
    """

    username: str
    password: str


class TokenResponse(BaseModel):
    """
    Token Response.

    Schema for the response containing access token and token type.
    """

    access_token: str
    token_type: str

    class Config:
        from_attributes = True
