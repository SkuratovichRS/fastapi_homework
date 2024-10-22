from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI, HTTPException

from app.advertisements.routers import advertisements_router
from app.core.database import close_orm, init_orm
from app.core.exceptions import http_exception_handler


async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_orm()
    print("Startup")
    yield
    await close_orm()
    print("Shutdown")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(advertisements_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
