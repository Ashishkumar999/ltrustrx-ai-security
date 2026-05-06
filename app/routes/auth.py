from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Temporary demo user database
users = {
    "admin": "admin123"
}


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if username in users and users[username] == password:

        response = RedirectResponse(
            url="/",
            status_code=302
        )

        response.set_cookie(
            key="user",
            value=username
        )

        return response

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid username or password"
        }
    )


@router.get("/logout")
async def logout():

    response = RedirectResponse(
        url="/login",
        status_code=302
    )

    response.delete_cookie("user")

    return response
