from fastapi import HTTPException

from app.advertisements.repository import Repository
from app.advertisements.schemas import (AdvertisementFiltersSchema,
                                        AdvertisementResponseSchema,
                                        CreateAdvertisementRequestSchema,
                                        UpdateAdvertisementRequestSchema)


class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    async def create(self, data: CreateAdvertisementRequestSchema) -> AdvertisementResponseSchema:
        advertisement = await self._repository.create(data.model_dump())
        return AdvertisementResponseSchema.model_validate(advertisement, from_attributes=True)

    async def update(
        self, advertisement_id: int, data: UpdateAdvertisementRequestSchema
    ) -> AdvertisementResponseSchema:
        advertisement = await self._repository.update(advertisement_id, data.model_dump(exclude_none=True))
        if not advertisement:
            raise HTTPException(status_code=404, detail="Advertisement not found")
        return AdvertisementResponseSchema.model_validate(advertisement, from_attributes=True)

    async def delete(self, advertisement_id: int) -> None:
        result = await self._repository.delete(advertisement_id)
        if not result:
            raise HTTPException(status_code=404, detail="Advertisement not found")

    async def get(self, advertisement_id: int) -> AdvertisementResponseSchema | None:
        advertisement = await self._repository.get(advertisement_id)
        if not advertisement:
            raise HTTPException(status_code=404, detail="Advertisement not found")
        return AdvertisementResponseSchema.model_validate(advertisement, from_attributes=True)

    async def search(self, data: AdvertisementFiltersSchema) -> list[AdvertisementResponseSchema]:
        advertisements = await self._repository.search(**data.model_dump(exclude_none=True))
        return [AdvertisementResponseSchema.model_validate(advertisement, from_attributes=True) for advertisement in advertisements]
