import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.permissions.models import Right, Role, Token, role_right, user_role
from app.users.models import User


class Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_by_name(self, name: str) -> User | None:
        stmt = select(User).where(User.name == name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_access_token(self, user_id: int, token: uuid.UUID) -> Token:
        token = Token(user_id=user_id, token=token)
        self._session.add(token)
        await self._session.commit()
        return token

    async def get_access_token(self, x_token: str) -> Token:
        stmt = select(Token).where(Token.token == x_token)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_right(self, write: bool, read: bool, only_owner: bool, model: str) -> Right:
        right = Right(write=write, read=read, only_owner=only_owner, model=model)
        self._session.add(right)
        await self._session.commit()
        return right

    async def create_role(self, name: str) -> Role:
        role = Role(name=name)
        self._session.add(role)
        await self._session.commit()
        return role

    async def create_user_role(self, user_id: int, role_id: int) -> None:
        stmt = user_role.insert().values(user_id=user_id, role_id=role_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def create_role_right(self, role_id: int, right_id: int) -> None:
        stmt = role_right.insert().values(role_id=role_id, right_id=right_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def add_user_role(self, user_id: int) -> None:
        stmt = select(Role).where(Role.name == "user")
        result = await self._session.execute(stmt)
        role = result.scalar_one_or_none()
        await self.create_user_role(user_id, role.id)

    async def add_admin_role(self, user_id: int) -> None:
        stmt = select(Role).where(Role.name == "admin")
        result = await self._session.execute(stmt)
        role = result.scalar_one_or_none()
        await self.create_user_role(user_id, role.id)

    async def check_rights(self, user_id: int, model: str, where_args: list[bool]) -> bool:
        stmt = (
            select((func.count(Right.id) > 0))
            .join(role_right, role_right.c.right_id == Right.id)
            .join(user_role, user_role.c.role_id == role_right.c.role_id)
            .where(Right.model == model)
            .where(user_role.c.user_id == user_id)
            .where(*where_args)
        )
        result = await self._session.execute(stmt)
        return result.scalar()
