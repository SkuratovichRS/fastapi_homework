from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException

from app.advertisements.routers import advertisements_router
from app.core.add_initial_data import add_initial_data
from app.core.database import DbSession, close_orm, init_orm
from app.core.exceptions import http_exception_handler
from app.permissions.repository import Repository
from app.permissions.routers import permissions_router
from app.permissions.service import Service
from app.users.routers import users_router

routers = [
    users_router,
    advertisements_router,
    permissions_router,
]


async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_orm()
    async with DbSession() as session:
        service = Service(Repository(session))
        await add_initial_data(service)
    print("db initialized")
    print("Startup")
    yield
    await close_orm()
    print("Shutdown")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(HTTPException, http_exception_handler)
for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
