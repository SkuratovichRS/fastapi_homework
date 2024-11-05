from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.advertisements.repository import Repository
from app.core.hash import hash_password
from app.users.schemas import (CreateUserRequestSchema,
                               UpdateUserRequestSchema, UserResponseSchema)


class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    async def create_user(self, data: CreateUserRequestSchema) -> UserResponseSchema:
        validated_data = data.model_dump()
        validated_data["password"] = hash_password(validated_data["password"])
        try:
            user = await self._repository.create_user(validated_data)
            return UserResponseSchema.model_validate(user, from_attributes=True)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User with this name already exists")
        

    async def get_user_by_id(self, user_id: int) -> UserResponseSchema:
        user = await self._repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseSchema.model_validate(user, from_attributes=True)

    async def update_user(self, user_id: int, data: UpdateUserRequestSchema) -> UserResponseSchema:
        validated_data = data.model_dump(exclude_none=True)
        if validated_data.get("password"):
            validated_data["password"] = hash_password(validated_data["password"])
        try:
            user = await self._repository.update_user(user_id, validated_data)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User with this name already exists")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseSchema.model_validate(user, from_attributes=True)
        
    async def delete_user(self, user_id: int) -> None:
        result = await self._repository.delete_user(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
                

