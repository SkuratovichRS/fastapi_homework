from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter

from app.advertisements.dependencies import ServiceDep
from app.advertisements.schemas import (AdvertisementFiltersSchema,
                                        AdvertisementResponseSchema,
                                        CreateAdvertisementRequestSchema,
                                        UpdateAdvertisementRequestSchema)

advertisements_router = APIRouter(prefix="/advertisements", tags=["advertisements"])


@advertisements_router.post("", response_model=AdvertisementResponseSchema, status_code=201)
async def create_advertisement(
    data: CreateAdvertisementRequestSchema, service: ServiceDep
) -> AdvertisementResponseSchema:
    return await service.create(data)


@advertisements_router.patch("/{advertisement_id}", response_model=AdvertisementResponseSchema)
async def update_advertisement(
    advertisement_id: int, data: UpdateAdvertisementRequestSchema, service: ServiceDep
) -> AdvertisementResponseSchema:
    return await service.update(advertisement_id, data)


@advertisements_router.delete("/{advertisement_id}", status_code=204)
async def delete_advertisement(advertisement_id: int, service: ServiceDep) -> None:
    await service.delete(advertisement_id)


@advertisements_router.get("/{advertisement_id}", response_model=AdvertisementResponseSchema)
async def get_advertisement(advertisement_id: int, service: ServiceDep) -> AdvertisementResponseSchema:
    return await service.get(advertisement_id)


@advertisements_router.get("", response_model=list[AdvertisementResponseSchema])
async def search_advertisements(
    service: ServiceDep,
    title: str | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    author_id: int | None = None,
    created_at: datetime | None = None,
) -> list[AdvertisementResponseSchema]:
    filters = AdvertisementFiltersSchema(
        title=title, description=description, price=price, author_id=author_id, created_at=created_at
    )
    return await service.search(filters)
