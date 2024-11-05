from fastapi import APIRouter

from app.permissions.dependencies import PermServiceDep
from app.permissions.schemas import LoginUserRequestSchema

permissions_router = APIRouter(prefix="/permissions", tags=["permissions"])


@permissions_router.post("/login", status_code=201, response_model=str)
async def login(data: LoginUserRequestSchema, perm_service: PermServiceDep) -> str:
    return await perm_service.login(data)
  