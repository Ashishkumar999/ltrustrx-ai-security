from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):

    role = request.cookies.get("role")

    if role != "admin":

        return HTMLResponse(
            content="""
            <h1>Access Denied</h1>
            <p>Admin access only</p>
            """,
            status_code=403
        )

    return templates.TemplateResponse(
        request=request,
        name="admin.html"
    )
