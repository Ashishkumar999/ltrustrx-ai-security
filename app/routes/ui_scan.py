from fastapi import APIRouter
from fastapi import Request
from fastapi import Form

from fastapi.templating import Jinja2Templates

from modules.scanner import run_healthcare_scan
from modules.database import save_scan_history

from modules.report_generator import generate_pdf_report

from datetime import datetime


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# RATE LIMIT STORE

RATE_LIMIT_TRACKER = {}


@router.post("/scan/ui")
async def ui_scan(

    request: Request,

    target: str = Form(...)

):

    user = request.cookies.get("user")


    # CHECK LOGIN

    if not user:

        return templates.TemplateResponse(

            request=request,

            name="login.html",

            context={

                "error": "Please login first"

            }

        )


    # RATE LIMITING

    current_time = datetime.now().timestamp()


    if user not in RATE_LIMIT_TRACKER:

        RATE_LIMIT_TRACKER[user] = []


    # KEEP ONLY LAST 60 SECONDS

    RATE_LIMIT_TRACKER[user] = [

        t for t in RATE_LIMIT_TRACKER[user]

        if current_time - t < 60

    ]


    # MAX 5 REQUESTS

    if len(RATE_LIMIT_TRACKER[user]) >= 5:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={

                "error":

                "Too many scan requests. Please wait."

            }

        )


    RATE_LIMIT_TRACKER[user].append(

        current_time

    )


    # RUN SCANNER

    results = run_healthcare_scan(target)


    summary = results["summary"]


    # SAVE TO DATABASE

    save_scan_history(

        username=user,

        target=target,

        total=summary["total"],

        high=summary["high"],

        medium=summary["medium"],

        low=summary["low"],

        info=summary["info"]

    )


    # GENERATE PDF REPORT

    report_file = generate_pdf_report(results)


    # RETURN PAGE

    return templates.TemplateResponse(

        request=request,

        name="index.html",

        context={

            "results": results,

            "report_file": report_file

        }

    )
