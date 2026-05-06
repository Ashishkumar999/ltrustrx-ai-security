from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes.api_scan import router as api_router
from app.routes.llm_scan import router as llm_router
from app.routes.ui_scan import router as ui_router
from app.routes.auth import router as auth_router

app = FastAPI()

app.mount("/reports", StaticFiles(directory="reports"), name="reports")

templates = Jinja2Templates(directory="templates")

# Include all routes
app.include_router(api_router)
app.include_router(llm_router)
app.include_router(ui_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    user = request.cookies.get("user")

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="login.html"
        )

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
