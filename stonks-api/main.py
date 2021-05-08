import logging
import os

from fastapi import FastAPI

from logger import InterceptHandler
from stonks_api.api.v1.api import api_router

# from loguru import logger

DEBUG = True if os.getenv("ENV", "production") == "development" else False
app = FastAPI(debug=DEBUG)


# logging.getLogger("uvicorn").handlers = []
# logging.getLogger("uvicorn").info("INFO MESSAGE")


for logger_name in logging.root.manager.loggerDict:
    if logger_name.startswith("uvicorn."):
        logging.getLogger(logger_name).handlers = []

handler = InterceptHandler()
logging.getLogger("uvicorn").handlers = [handler]
logging.getLogger("uvicorn.access").handlers = [handler]

# logging.getLogger("uvicorn").info("my maaan")
# logging.getLogger("uvicorn").addHandler(InterceptHandler())
# logging.getLogger("uvicorn").addHandler(InterceptHandler())
# logging.getLogger("uvicorn").info("my maaan")
# loggers = {logger for logger in logging.root.manager.loggerDict if logger.startswith("uvicorn")}
# logging.getLogger("uvicorn").info(loggers)
#
# logging.getLogger("uvicorn").info(logging.getLogger("uvicorn").handlers)
# logging.getLogger("uvicorn").info(logging.getLogger("uvicorn.error").handlers)
# logging.getLogger("uvicorn").info(logging.getLogger("uvicorn.asgi").handlers)
# logging.getLogger("uvicorn").info(logging.getLogger("uvicorn.access").handlers)


@app.get("/")
async def index():
    return {"message": "SWEET HOME ALABAMA"}


# app.include_router(api_router, prefix="/v1", dependencies=[Depends(logging_dependency)])
app.include_router(api_router, prefix="/v1")
