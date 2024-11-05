from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


class Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, validated_data: dict) -> User:
        user = User(**validated_data)
        self._session.add(user)
        await self._session.commit()
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, validated_data: dict) -> User | None:
        stmt = update(User).where(User.id == user_id).values(**validated_data).returning(User)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one_or_none()

    async def delete_user(self, user_id: int) -> bool:
        stmt = delete(User).where(User.id == user_id).returning(User.id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        deleted_user = result.scalar_one_or_none()
        return deleted_user is not None

   