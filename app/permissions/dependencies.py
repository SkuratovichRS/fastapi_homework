import uuid
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_session
from app.permissions.models import Token
from app.permissions.repository import Repository
from app.permissions.service import Service


def get_repository(session: AsyncSession = Depends(get_session)) -> Repository:
    return Repository(session)


def get_service(repository: Repository = Depends(get_repository)) -> Service:
    return Service(repository)


async def get_access_token(x_token: Annotated[uuid.UUID, Header()], service: Service = Depends(get_service)) -> Token:
    return await service.get_access_token(x_token)


PermServiceDep = Annotated[Service, Depends(get_service)]
AccessTokenDependency = Annotated[Token, Depends(get_access_token)]
