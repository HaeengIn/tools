import logging
from logging import Logger

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from tools.exceptions import Error
from tools.router.index import router as IndexRouter

logger: Logger = logging.getLogger(__name__)


app = FastAPI(title="Tools")
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


@app.exception_handler(Error)
def ErrorHandler(
    request: Request,
    exception: Error,
):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
        },
    )


app.include_router(IndexRouter)


def main() -> None:
    uvicorn(
        "tools:app",
        host="0.0.0.0",
        port=8000,
    )
