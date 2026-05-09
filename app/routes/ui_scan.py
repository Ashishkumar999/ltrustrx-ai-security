from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from modules.llm_tester import scan_llm
from modules.pdf_report import generate_pdf_report
from modules.logger import write_log
from modules.database import save_scan_history

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/scan/ui", response_class=HTMLResponse)
async def run_ui_scan(request: Request):

    username = request.cookies.get("user", "anonymous")

    write_log("LLM_SCAN_EXECUTED", username)

    results = scan_llm()

    username = request.cookies.get("user", "anonymous")

    summary = results.get("summary", {})

    save_scan_history(

    username=username,

    target="Healthcare AI LLM",

    total_issues=summary.get("total", 0),

    high=summary.get("high", 0),

    medium=summary.get("medium", 0),

    low=summary.get("low", 0),

    info=summary.get("info", 0),

    report_path=results.get("pdf_report", "")

     )
    pdf_path = generate_pdf_report(results)

    results["pdf_report"] = pdf_path

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": results
        }
    )
