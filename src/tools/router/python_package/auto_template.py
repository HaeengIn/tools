from auto_template import setup_templates
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Python Packages"])
templates: Jinja2Templates = setup_templates(directory="templates")


@router.get(
    "/python-package/auto-template",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def auto_template(request: Request) -> HTMLResponse:
    css_file: list[str] = [
        "auto-template/index.css",
    ]

    js_file: list[str] = [
        "auto-template/index.js",
    ]

    context: dict = {
        "title": "auto-template - Streamline your Jinja2 template setup.",
        "css_file": css_file,
        "js_file": js_file,
    }

    try:
        return templates.TemplateResponse(
            request=request,
            context=context,
            name="python-package/auto-template/index.j2",
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Server error has occured: {e}",
            status_code=500,
        )
