from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from modules.database import (
    init_db,
    create_user,
    validate_user
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Initialize database
init_db()


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

    user = validate_user(username, password)

    if user:

        response = RedirectResponse(
            url="/",
            status_code=302
        )

        response.set_cookie(
            key="user",
            value=username
        )

        response.set_cookie(
            key="role",
            value=user["role"]
       )

        return response

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid username or password"
        }
    )


@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html"
    )

@router.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    role = "user"

    if username == "admin":
        role = "admin"

    success = create_user(
        username,
        password,
        role
    )

    if success:

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    return templates.TemplateResponse(
        request=request,
        name="signup.html",
        context={
            "error": "Username already exists"
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
