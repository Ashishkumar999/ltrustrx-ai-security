from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.llm_tester import scan_llm

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/scan/ui", response_class=HTMLResponse)
async def run_ui_scan(request: Request):

    results = scan_llm()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": results
        }
    )
