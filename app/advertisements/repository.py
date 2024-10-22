from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.advertisements.models import Advertisement


class Repository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, validated_data: dict) -> Advertisement:
        advertisement = Advertisement(**validated_data)
        self._session.add(advertisement)
        await self._session.commit()
        await self._session.refresh(advertisement)
        return advertisement

    async def update(self, advertisement_id: int, validated_data: dict) -> Advertisement | None:
        advertisement = await self._session.get(Advertisement, advertisement_id)
        if not advertisement:
            return None
        for key, value in validated_data.items():
            setattr(advertisement, key, value)
        await self._session.commit()
        return advertisement
    
    async def delete(self, advertisement_id: int) -> bool:
        advertisement = await self._session.get(Advertisement, advertisement_id)
        if not advertisement:
            return False
        await self._session.delete(advertisement)
        await self._session.commit()
        return True

    async def get(self, advertisement_id: int) -> Advertisement | None:
        return await self._session.get(Advertisement, advertisement_id)

    async def search(self, **kwargs) -> list[Advertisement]:
        stmt = select(Advertisement).filter_by(**kwargs)
        result = await self._session.execute(stmt)
        return result.scalars().all()
