from auto_template import setup_templates
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Index"])
templates: Jinja2Templates = setup_templates(directory="templates")

@router.get("/")
async def Index(request: Request) -> HTMLResponse:
    context = {
        "title": "Tools by HaeengIn",
    }

    return templates.TemplateResponse(
        request=request,
        context=context,
        name="index.jinja2",
    )
