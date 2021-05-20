import logging
import os

from fastapi import FastAPI, Request
from fastapi.params import Depends
from loguru import logger

from logger import InterceptHandler
from stonks_api.api.v1.api import api_router
from starlette.routing import Match

from stonks_api.database import create_no_device

DEBUG = True if os.getenv("ENV", "production") == "development" else False
app = FastAPI(debug=DEBUG)

for logger_name in logging.root.manager.loggerDict:
    if logger_name.startswith("uvicorn."):
        logging.getLogger(logger_name).handlers = []

handler = InterceptHandler()
logging.getLogger("uvicorn").handlers = [handler]
logging.getLogger("uvicorn.access").handlers = [handler]


async def log_middle(request: Request):
    logger.debug(f"{request.method} {request.url}")
    routes = request.app.router.routes

    logger.debug("Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")

    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    logger.debug("Body:")
    logger.debug(await request.body())


@app.on_event("startup")
async def on_startup():
    create_no_device()


@app.get("/")
async def index():
    return {"message": "SWEET HOME ALABAMA"}


app.include_router(api_router, prefix="/v1", dependencies=[Depends(log_middle)])
