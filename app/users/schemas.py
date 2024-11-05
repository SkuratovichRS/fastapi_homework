from pydantic import BaseModel


class CreateUserRequestSchema(BaseModel):
    name: str
    password: str

class UserResponseSchema(BaseModel):
    id: int
    name: str

class UpdateUserRequestSchema(BaseModel):
    name: str | None = None
    password: str | None = None