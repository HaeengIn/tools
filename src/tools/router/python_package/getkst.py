from auto_template import setup_templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from tools.exceptions import Error

router = APIRouter(tags=["Python Package"])
template: Jinja2Templates = setup_templates(directory="templates")


@router.get(
    "/python-package/getKST",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def getKST(request: Request) -> HTMLResponse:
    css_file: list[str] = [
        "getkst/index.css",
    ]

    js_file: list[str] = [
        "getkst/index.js",
    ]

    context: dict = {
        "title": "getKST - Most easiest way to get Asia/Seoul timezone data",
        "css_file": css_file,
        "js_file": js_file,
    }

    try:
        return template.TemplateResponse(
            request=request,
            context=context,
            name="python-package/getkst/index.j2",
        )
    except Exception as e:
        raise Error(
            f"Server error has occured: {e}",
            500,
        )
