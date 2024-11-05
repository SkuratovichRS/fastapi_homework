from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.users.repository import Repository
from app.users.service import Service


def get_repository(session: AsyncSession = Depends(get_session)) -> Repository:
    return Repository(session)


def get_service(repository: Repository = Depends(get_repository)) -> Service:
    return Service(repository)


UsersServiceDep = Annotated[Service, Depends(get_service)]