import logging
from logging import Logger

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

from tools.exceptions import Error
from tools.router.image_converter.toavif import router as toAVIFRouter
from tools.router.index import router as IndexRouter
from tools.router.python_package.auto_template import router as auto_templateRouter
from tools.router.python_package.getkst import router as getKSTRouter

logger: Logger = logging.getLogger(__name__)


class LowercaseURLMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request.scope["path"] = request.url.path.lower()
        return await call_next(request)


app = FastAPI(title="Tools")
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)
app.add_middleware(LowercaseURLMiddleware)


@app.exception_handler(Error)
def ErrorHandler(
    request: Request,
    exception: Error,
) -> JSONResponse:
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
        },
    )


app.include_router(IndexRouter)
app.include_router(getKSTRouter)
app.include_router(auto_templateRouter)
app.include_router(toAVIFRouter)


def main() -> None:
    uvicorn.run(
        "tools:app",
        host="0.0.0.0",
        port=8000,
    )
