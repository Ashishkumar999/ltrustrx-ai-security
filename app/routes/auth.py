from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from modules.database import (
    create_user,
    validate_user
)

from modules.logger import write_log

from modules.security import (
    is_blocked,
    record_failed_attempt,
    reset_attempts
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login")
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.post("/login")
async def login_post(request: Request):

    form = await request.form()

    username = form.get("username")

    password = form.get("password")

    # RATE LIMIT CHECK

    if is_blocked(username):

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "error": "Too many failed attempts. Try again later."
            }
        )

    user = validate_user(username, password)

    if user:

        reset_attempts(username)

        write_log("LOGIN_SUCCESS", username)

        response = RedirectResponse(
            url="/",
            status_code=303
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

    # FAILED LOGIN

    record_failed_attempt(username)

    write_log("LOGIN_FAILED", username)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid username or password"
        }
    )


@router.get("/signup")
async def signup_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="signup.html"
    )


@router.post("/signup")
async def signup_post(request: Request):

    form = await request.form()

    username = form.get("username")

    password = form.get("password")

    create_user(username, password)

    write_log("SIGNUP", username)

    return RedirectResponse(
        url="/login",
        status_code=303
    )


@router.get("/logout")
async def logout():

    response = RedirectResponse(
        url="/login",
        status_code=303
    )

    response.delete_cookie("user")

    response.delete_cookie("role")

    return response
