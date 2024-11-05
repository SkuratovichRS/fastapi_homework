from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Request

from app.advertisements.dependencies import AdvServiceDep
from app.advertisements.schemas import (AdvertisementFiltersSchema,
                                        AdvertisementResponseSchema,
                                        CreateAdvertisementRequestSchema,
                                        UpdateAdvertisementRequestSchema)
from app.core.check_rights import check_rights
from app.permissions.dependencies import AccessTokenDependency, PermServiceDep

advertisements_router = APIRouter(prefix="/advertisements", tags=["advertisements"])


@advertisements_router.post("", response_model=AdvertisementResponseSchema, status_code=201)
async def create_advertisement(
    request: Request,
    data: CreateAdvertisementRequestSchema,
    adv_service: AdvServiceDep,
    perm_service: PermServiceDep,
    token: AccessTokenDependency,
) -> AdvertisementResponseSchema:
    user_id = token.user_id
    await check_rights(request, perm_service, user_id)
    return await adv_service.create(user_id, data)


@advertisements_router.patch("/{advertisement_id}", response_model=AdvertisementResponseSchema)
async def update_advertisement(
    request: Request,
    advertisement_id: int,
    data: UpdateAdvertisementRequestSchema,
    adv_service: AdvServiceDep,
    perm_service: PermServiceDep,
    token: AccessTokenDependency,
) -> AdvertisementResponseSchema:
    user_id = token.user_id
    adv = await adv_service.get(advertisement_id)
    obj_id = adv.author_id
    await check_rights(request, perm_service, user_id, obj_id)
    return await adv_service.update(advertisement_id, data)


@advertisements_router.delete("/{advertisement_id}", status_code=204)
async def delete_advertisement(
    request: Request,
    advertisement_id: int,
    adv_service: AdvServiceDep,
    perm_service: PermServiceDep,
    token: AccessTokenDependency,
) -> None:
    user_id = token.user_id
    adv = await adv_service.get(advertisement_id)
    obj_id = adv.author_id
    await check_rights(request, perm_service, user_id, obj_id)
    await adv_service.delete(advertisement_id)


@advertisements_router.get("/{advertisement_id}", response_model=AdvertisementResponseSchema)
async def get_advertisement(advertisement_id: int, adv_service: AdvServiceDep) -> AdvertisementResponseSchema:
    return await adv_service.get(advertisement_id)


@advertisements_router.get("", response_model=list[AdvertisementResponseSchema])
async def search_advertisements(
    adv_service: AdvServiceDep,
    title: str | None = None,
    description: str | None = None,
    price: Decimal | None = None,
    author_id: int | None = None,
    created_at: datetime | None = None,
) -> list[AdvertisementResponseSchema]:
    filters = AdvertisementFiltersSchema(
        title=title, description=description, price=price, author_id=author_id, created_at=created_at
    )
    return await adv_service.search(filters)
