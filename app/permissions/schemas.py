from pydantic import BaseModel


class LoginUserRequestSchema(BaseModel):
    name: str
    password: str
    is_admin: bool = False