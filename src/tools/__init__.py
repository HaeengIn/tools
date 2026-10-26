import logging
from logging import Logger

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from requests.sessions import Request

from tools.router.index import router as IndexRouter

logger: Logger = logging.getLogger(__name__)


class Error(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        self.message: str = message
        self.status_code: int = status_code
        super().__init__(message)


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
        port="8000",
    )
