from auto_template import setup_templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Index"])
templates: Jinja2Templates = setup_templates(directory="templates")


@router.get(
    "/",
    include_in_schema=False,
    response_class=HTMLResponse,
)
async def Index(request: Request) -> HTMLResponse:
    css_file: list[str] = [
        "index/index",
    ]

    context: dict = {
        "title": "Tools by HaeengIn",
        "css_file": css_file,
    }

    return templates.TemplateResponse(
        request=request,
        context=context,
        name="index.jinja2",
    )
