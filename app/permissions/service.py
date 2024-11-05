import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.hash import verify_password
from app.core.settings import Settings
from app.permissions.models import Right, Role
from app.permissions.repository import Repository
from app.permissions.schemas import LoginUserRequestSchema


class Service:

    def __init__(self, repository: Repository):
        self._repository = repository

    async def authenticate_user(self, name: str, password: str) -> int:
        user = await self._repository.get_user_by_name(name)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user.id

    async def login(self, data: LoginUserRequestSchema) -> str:
        user_id = await self.authenticate_user(data.name, data.password)
        access_token = await self._repository.create_access_token(user_id, uuid.uuid4())
        if data.is_admin:
            await self._repository.add_admin_role(user_id)
        else:
            await self._repository.add_user_role(user_id)
        return str(access_token.token)

    async def get_access_token(self, x_token: str) -> str:
        token = await self._repository.get_access_token(x_token)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid token")
        if datetime.datetime.now() > token.created_at + datetime.timedelta(hours=Settings.TTL_HOURS):
            raise HTTPException(status_code=401, detail="Token expired")
        return token

    async def check_rights(
        self,
        user_id: int,
        method: str,
        model: str,
        obj_id: int | None = None,
    ) -> bool:
        if method == "GET":
            where_args = [Right.read == True]
            if not await self._repository.check_rights(user_id, model, where_args):
                raise HTTPException(status_code=403, detail="Access denied")
            return
        if method == "POST":
            where_args = [Right.write == True]
            if not await self._repository.check_rights(user_id, model, where_args):
                raise HTTPException(status_code=403, detail="Access denied")
            return
        if method in ["PATCH", "DELETE"]:
            where_args = [Right.only_owner == False]
            if await self._repository.check_rights(user_id, model, where_args):
                return
            where_args = [Right.only_owner == True]
            if await self._repository.check_rights(user_id, model, where_args):
                if obj_id == user_id:
                    return
        raise HTTPException(status_code=403, detail="Access denied")

    async def create_roles(self) -> list[Role]:
        try:
            return [
                await self._repository.create_role(name="user"),
                await self._repository.create_role(name="admin"),
            ]
        except IntegrityError:
            return []

    async def create_right(self, write: bool, read: bool, only_owner: bool, model: str) -> Right:
        return await self._repository.create_right(write=write, read=read, only_owner=only_owner, model=model)

    async def create_role_right(self, role_id: int, right_id: int) -> None:
        await self._repository.create_role_right(role_id, right_id)
