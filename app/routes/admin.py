from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from modules.database import get_scan_history

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/admin")
async def admin_dashboard(request: Request):

    role = request.cookies.get("role")

    if role != "admin":

        return templates.TemplateResponse(
            request=request,
            name="access_denied.html"
        )

    scans = get_scan_history()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "scans": scans
        }
    )
