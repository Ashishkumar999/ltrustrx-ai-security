from fastapi import APIRouter
from fastapi import Request
from fastapi import Form

from fastapi.templating import Jinja2Templates

from modules.scanner import run_healthcare_scan

from datetime import datetime


router = APIRouter()

templates = Jinja2Templates(directory="templates")


SCAN_HISTORY = []


@router.get("/scan/ui")
async def scan_ui(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="index.html"

    )


@router.post("/scan/ui")
async def run_scan(

    request: Request,

    target: str = Form(...)

):

    results = run_healthcare_scan(target)


    SCAN_HISTORY.insert(

        0,

        {

            "username": "admin",

            "target": target,

            "total": results["summary"]["total"],

            "high": results["summary"]["high"],

            "medium": results["summary"]["medium"],

            "low": results["summary"]["low"],

            "info": results["summary"]["info"],

            "created_at": datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        }

    )


    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={

            "results": results

        }

    )


@router.get("/admin")
async def admin_dashboard(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="admin.html",

        context={

            "scans": SCAN_HISTORY

        }

    )
