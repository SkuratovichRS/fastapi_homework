from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.advertisements.repository import Repository
from app.advertisements.service import Service
from app.core.dependencies import get_session


def get_repository(session: AsyncSession = Depends(get_session)) -> Repository:
    return Repository(session)


def get_service(repository: Repository = Depends(get_repository)) -> Service:
    return Service(repository)


ServiceDep = Annotated[Service, Depends(get_service)]
