import asyncio
import os
import secrets
import time
import uuid
import zipfile
from asyncio.events import AbstractEventLoop
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

import aiofiles
import httpx
import pyvips
from auto_template import setup_templates
from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from httpx._models import Response
from pyvips.vimage import Image

from tools.exceptions import Error

load_dotenv()

router = APIRouter(tags=["Image Converter"])
templates: Jinja2Templates = setup_templates(directory="templates")

UPLOAD_DIR = Path("uploads/toavif")
CONVERTED_DIR = Path("converted/toavif")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
CONVERTED_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TURNSTILE_SECRET_KEY: str | None = os.getenv("TURNSTILE_SECRET_KEY")
TURNSTILE_SITE_KEY: str | None = os.getenv("TURNSTILE_SITE_KEY")
TURNSTILE_URL: str = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
SESSION_TTL: int = 3600
MAX_FILES: int = 100
ANIMATED_EXTS: list[str] = [
    ".gif",
    ".webp",
    ".apng",
    ".png",
]


@dataclass
class JobStatus:
    job_id: str
    total_files: int
    processed_files: int = 0
    current_file: str = ""
    current_file_progress: float = 0.0
    status: str = "processing"
    files: list[str] = field(default_factory=list)
    error: str = ""

    def to_sse(self) -> str:
        import json

        return "data: {}\n\n".format(
            json.dumps(
                {
                    "status": self.status,
                    "current_file": self.current_file,
                    "current_file_progress": round(self.current_file_progress, 1),
                    "overall_progress": round(
                        (self.processed_files / max(self.total_files, 1)) * 100, 1
                    ),
                    "processed_files": self.processed_files,
                    "total_files": self.total_files,
                    "files": self.files,
                    "error": self.error,
                },
                ensure_ascii=False,
            )
        )


sessions: dict[str, float] = {}
jobs: dict[str, JobStatus] = {}


def _cleanup_sessions() -> None:
    now: float = time.time()
    for k in [k for k, v in sessions.items() if v < now]:
        del sessions[k]


def _convert_to_avif(input_path: str, output_path: str, job: JobStatus) -> None:
    ext: str = Path(input_path).suffix.lower()

    def on_eval(image, progress) -> None:
        job.current_file_progress = progress.percent

    if ext in ANIMATED_EXTS:
        try:
            image: Image = pyvips.Image.new_from_file(
                input_path, n=-1, access="sequential"
            )
            n_pages: (
                Image | bool | float | int | list[Image] | list[float] | list[int] | str
            ) = image.get("n-pages") if image.get_typeof("n-pages") else 1

            if int(n_pages) > 1:
                image.set_progress(True)
                image.signal_connect("eval", on_eval)
                image.write_to_file(output_path, Q=80)
                return
        except pyvips.Error:
            pass

    image = pyvips.Image.new_from_file(input_path, access="sequential")
    image.set_progress(True)
    image.signal_connect("eval", on_eval)
    image.write_to_file(output_path, Q=80)


async def _process_images(
    job_id: str,
    file_names: list[str],
    job_dir: Path,
    converted_dir: Path,
) -> None:
    job: JobStatus = jobs[job_id]

    try:
        used_out_names: set[str] = set()

        for name in file_names:
            stem: str = Path(name).stem
            out_name: str = f"{stem}.avif"
            counter: int = 1

            while out_name in used_out_names:
                out_name = f"{stem}_{counter}.avif"
                counter += 1

            used_out_names.add(out_name)
            job.current_file = name
            job.current_file_progress = 0.0

            loop: AbstractEventLoop = asyncio.get_running_loop()

            await loop.run_in_executor(
                None,
                _convert_to_avif,
                str(job_dir / name),
                str(converted_dir / out_name),
                job,
            )

            job.processed_files += 1
            job.current_file_progress = 100.0
            job.files.append(out_name)

        job.status = "done"
    except Exception as e:
        job.status = "error"
        job.error = str(e)


@router.get(
    "/toavif",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def toAVIF(request: Request) -> HTMLResponse:
    css_file: list[str] = [
        "image-converter/toavif/index.css",
    ]

    js_file: list[str] = [
        "image-converter/toavif/turnstile.js",
        "image-converter/toavif/index.js",
        "image-converter/toavif/upload.js",
        "image-converter/toavif/progress.js",
    ]

    context: dict = {
        "title": "toAVIF - Convert you images to AVIF images",
        "css_file": css_file,
        "js_file": js_file,
        "TURNSTILE_SITE_KEY": TURNSTILE_SITE_KEY,
    }

    try:
        return templates.TemplateResponse(
            request=request,
            context=context,
            name="image-converter/toavif.j2",
        )
    except Exception as e:
        raise Error(
            f"Server error has occured: {e}",
            500,
        )


@router.post("/toavif/verify")
async def VerifyTurnstile(token: str = Form(...)) -> dict[str, str | int]:
    async with httpx.AsyncClient() as client:
        response: Response = await client.post(
            TURNSTILE_URL,
            data={"secret": TURNSTILE_SECRET_KEY, "response": token},
        )
    if not response.json().get("success"):
        raise Error(
            "Failed to verify Cloudflare Turnstile",
            400,
        )

    _cleanup_sessions()
    session_token: str = secrets.token_urlsafe(32)
    sessions[session_token] = time.time() + SESSION_TTL
    return {"session_token": session_token, "expires_in": SESSION_TTL}


@router.post("/toavif/upload")
async def UploadImages(
    files: list[UploadFile],
    session_token: str = Form(...),
) -> dict[str, str]:
    expires_at: float | None = sessions.get(session_token)

    if not expires_at or expires_at < time.time():
        sessions.pop(session_token, None)

        raise Error(
            "Session is expired or not valid.",
            401,
        )

    if not files:
        raise Error(
            "There are no images.",
            400,
        )

    if len(files) > MAX_FILES:
        raise Error(
            f"You can upload up to {MAX_FILES} images.",
            400,
        )

    job_id = str(uuid.uuid4())
    job_dir: Path = UPLOAD_DIR / job_id
    converted_dir: Path = CONVERTED_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    converted_dir.mkdir(parents=True, exist_ok=True)

    saved: list[str] = []
    for file in files:
        name: str = Path(file.filename or "image").name
        dest: Path = job_dir / name

        if dest.exists():
            stem: str = Path(name).stem
            suffix: str = Path(name).suffix
            counter: int = 1

            while dest.exists():
                name = f"{stem}_{counter}{suffix}"
                dest = job_dir / name
                counter += 1

        dest.write_bytes(await file.read())
        saved.append(name)

    job = JobStatus(job_id=job_id, total_files=len(saved))
    jobs[job_id] = job
    asyncio.create_task(_process_images(job_id, saved, job_dir, converted_dir))

    return {"job_id": job_id}


@router.get("/toavif/progress/{job_id}")
async def stream_progress(job_id: str) -> StreamingResponse:
    if job_id not in jobs:
        raise Error(
            "Cannot find process.",
            404,
        )

    async def _generate() -> AsyncGenerator[str, None]:
        while True:
            job: JobStatus | None = jobs.get(job_id)

            if not job:
                yield 'data: {"status": "error"}\n\n'
                break

            yield job.to_sse()

            if job.status in ("done", "error"):
                break

            await asyncio.sleep(0.3)

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


@router.get("/toavif/download/{job_id}/{filename:path}")
async def download_file(job_id: str, filename: str) -> StreamingResponse:
    job_dir: Path = CONVERTED_DIR / job_id

    if not job_dir.is_dir():
        raise Error(
            "Cannot find image.",
            404,
        )

    file_path: Path | None = next(
        (
            path
            for path in job_dir.iterdir()
            if path.is_file() and path.name.casefold() == filename.casefold()
        ),
        None,
    )

    if file_path is None:
        raise Error(
            "Cannot find image.",
            404,
        )

    async def _stream() -> AsyncGenerator[bytes, None]:
        async with aiofiles.open(
            file_path,
            "rb",
        ) as file:
            while True:
                chunk: bytes = await file.read(65536)

                if not chunk:
                    break

                yield chunk

    return StreamingResponse(
        _stream(),
        media_type="image/avif",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}",
            "Content-Length": str(file_path.stat().st_size),
        },
    )


@router.get("/toavif/download/{job_id}")
async def download_zip(job_id: str) -> StreamingResponse:
    job: JobStatus | None = jobs.get(job_id)

    if not job or job.status != "done":
        raise Error(
            "Cannot find completed process.",
            404,
        )

    converted_dir: Path = CONVERTED_DIR / job_id

    def _build_zip() -> bytes:
        buf: BytesIO = BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname in job.files:
                fp: Path = converted_dir / fname

                if fp.is_file():
                    zf.write(fp, fname)

        return buf.getvalue()

    data: bytes = await asyncio.get_running_loop().run_in_executor(None, _build_zip)
    zip_name: str = f"toAVIF_{job_id}.zip"

    async def _stream() -> AsyncGenerator[bytes, None]:
        yield data

    return StreamingResponse(
        _stream(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{quote(zip_name)}",
            "Content-Length": str(len(data)),
        },
    )
