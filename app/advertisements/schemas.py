from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateAdvertisementRequestSchema(BaseModel):
    title: str
    description: str
    price: Decimal
    author_id: int

class UpdateAdvertisementRequestSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None

class AdvertisementResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    author_id: int
    created_at: datetime


class AdvertisementFiltersSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None
    author_id: int | None = None
    created_at: datetime | None = None

