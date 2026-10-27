from auto_template import setup_templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from tools.exceptions import Error

router = APIRouter(tags=["Python Packages"])
templates: Jinja2Templates = setup_templates(directory="templates")


@router.get(
    "/python-package/auto-template",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def auto_template(request: Request) -> HTMLResponse:
    css_file: list[str] = [
        "python-package/auto-template/index.css",
    ]

    js_file: list[str] = [
        "python-package/auto-template/index.js",
    ]

    context: dict = {
        "title": "auto-template - Streamline your Jinja2 template setup.",
        "css_file": css_file,
        "js_file": js_file,
        "package_name": "auto-template",
        "package_desc": "Fastest way to set up Jinja2 Templates",
        "package_pypi_name": "auto_template",
    }

    try:
        return templates.TemplateResponse(
            request=request,
            context=context,
            name="python-package/auto-template/index.j2",
        )
    except Exception as e:
        raise Error(
            f"Server error has occured: {e}",
            status_code=500,
        )
