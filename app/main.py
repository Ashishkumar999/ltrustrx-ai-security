from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routes.api_scan import router as api_router
from app.routes.llm_scan import router as llm_router
from app.routes.ui_scan import router as ui_router

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Include all routes
app.include_router(api_router)
app.include_router(llm_router)
app.include_router(ui_router)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )
