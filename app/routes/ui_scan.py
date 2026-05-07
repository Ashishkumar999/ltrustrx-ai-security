from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.llm_tester import scan_llm
from modules.pdf_report import generate_pdf_report
from modules.logger import write_log

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/scan/ui", response_class=HTMLResponse)
async def run_ui_scan(request: Request):

    username = request.cookies.get("user", "anonymous")

    write_log("LLM_SCAN_EXECUTED", username)

    results = scan_llm()

    pdf_path = generate_pdf_report(results)

    results["pdf_report"] = pdf_path

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": results
        }
    )
