from fastapi import APIRouter
from fastapi import Form
from fastapi import Request

from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from modules.database import create_user
from modules.database import validate_user

from modules.jwt_handler import create_access_token


router = APIRouter()

templates = Jinja2Templates(directory="templates")


# LOGIN PAGE

@router.get("/login")
async def login_page(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="login.html",

        context={}

    )


# SIGNUP PAGE

@router.get("/signup")
async def signup_page(request: Request):

    return templates.TemplateResponse(

        request=request,

        name="signup.html",

        context={}

    )


# SIGNUP

@router.post("/signup")
async def signup(

    username: str = Form(...),

    password: str = Form(...)

):

    create_user(

        username=username,

        password=password

    )

    return RedirectResponse(

        url="/login",

        status_code=303

    )


# LOGIN

@router.post("/login")
async def login(

    username: str = Form(...),

    password: str = Form(...)

):

    valid = validate_user(

        username,

        password

    )


    if not valid:

        return RedirectResponse(

            url="/login",

            status_code=303

        )


    # CREATE JWT TOKEN

    token = create_access_token({

        "sub": username

    })


    response = RedirectResponse(

        url="/",

        status_code=303

    )


    # USER COOKIE

    response.set_cookie(

        key="user",

        value=username,

        httponly=True

    )


    # JWT COOKIE

    response.set_cookie(

        key="access_token",

        value=token,

        httponly=True

    )


    return response


# LOGOUT

@router.get("/logout")
async def logout():

    response = RedirectResponse(

        url="/login",

        status_code=303

    )

    response.delete_cookie("user")

    response.delete_cookie("access_token")

    return response
