from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routes.api_scan import router as api_router
from app.routes.llm_scan import router as llm_router
from app.routes.ui_scan import router as ui_router
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router


app = FastAPI()

templates = Jinja2Templates(directory="templates")


# SECURITY HEADERS

class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        response = await call_next(request)

        response.headers["X-Frame-Options"] = "DENY"

        response.headers["X-Content-Type-Options"] = "nosniff"

        response.headers["Referrer-Policy"] = "no-referrer"

        response.headers["Content-Security-Policy"] = (
            "default-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"
        )

        return response


app.add_middleware(SecurityHeadersMiddleware)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# STATIC FILES

app.mount("/reports", StaticFiles(directory="reports"), name="reports")


# INCLUDE ROUTES

app.include_router(api_router)

app.include_router(llm_router)

app.include_router(ui_router)

app.include_router(auth_router)

app.include_router(admin_router)


# HOME PAGE

@app.get("/")
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "results": None
        }
    )
