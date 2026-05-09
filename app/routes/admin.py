from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from modules.database import get_scan_history


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/admin")
async def admin_dashboard(request: Request):

    history = get_scan_history()


    return templates.TemplateResponse(

        request=request,

        name="admin.html",

        context={

            "history": history

        }

    )
