from fastapi import APIRouter, Request

from app.core.check_rights import check_rights
from app.permissions.dependencies import AccessTokenDependency, PermServiceDep
from app.users.dependencies import UsersServiceDep
from app.users.schemas import (CreateUserRequestSchema,
                               UpdateUserRequestSchema, UserResponseSchema)

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("", status_code=201, response_model=UserResponseSchema)
async def create_user(data: CreateUserRequestSchema, users_service: UsersServiceDep) -> UserResponseSchema:
    return await users_service.create_user(data)


@users_router.get("/{user_id}", status_code=200, response_model=UserResponseSchema)
async def get_user(user_id: int, user_service: UsersServiceDep) -> UserResponseSchema:
    return await user_service.get_user_by_id(user_id)


@users_router.patch("/{user_id}", status_code=200, response_model=UserResponseSchema)
async def update_user(
    request: Request,
    user_id: int,
    data: UpdateUserRequestSchema,
    user_service: UsersServiceDep,
    perm_service: PermServiceDep,
    token: AccessTokenDependency,
) -> UserResponseSchema:
    obj_id = user_id
    user_id = token.user_id
    await check_rights(request, perm_service, user_id, obj_id)
    return await user_service.update_user(obj_id, data)


@users_router.delete("/{user_id}", status_code=204)
async def delete_user(
    request: Request,
    user_id: int,
    user_service: UsersServiceDep,
    perm_service: PermServiceDep,
    token: AccessTokenDependency,
) -> None:
    obj_id = user_id
    user_id = token.user_id
    await check_rights(request, perm_service, user_id, obj_id)
    await user_service.delete_user(obj_id)
