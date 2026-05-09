from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from modules.scanner import run_healthcare_scan
from modules.database import save_scan_history


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/scan/ui")
async def scan_ui(request: Request):

    form = await request.form()

    target = form.get("target")

    username = request.cookies.get("user", "anonymous")

    results = run_healthcare_scan(target)

    summary = results.get("summary", {})

    save_scan_history(

        username=username,

        target=target,

        total_issues=summary.get("total", 0),

        high=summary.get("high", 0),

        medium=summary.get("medium", 0),

        low=summary.get("low", 0),

        info=summary.get("info", 0),

        report_path=results.get("pdf_report", "")

    )

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={

            "results": results

        }

    )
