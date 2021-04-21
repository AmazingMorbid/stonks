import logging

from fastapi import FastAPI

from stonks_api.api.v1.api import api_router
from stonks_api.database import engine
from stonks_api.models import Base


Base.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


@app.get("/")
async def index():
    return {"message": "SWEET HOME ALABAMA"}


app.include_router(api_router, prefix="/v1")
