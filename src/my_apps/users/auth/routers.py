from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from src.db.db_deps import get_session
from src.dependencies import get_templates
from src.my_apps.users.auth.authentication import authenticate_user
from src.my_apps.users.auth.forms import register_user_form
from src.my_apps.users.crud import crud_user
from src.my_apps.users.schemas import UserRegistrate

router = APIRouter(tags=['users/auth'])


@router.get('/signup', response_class=HTMLResponse, status_code=status.HTTP_200_OK, name='show_signup_form')
async def show_signup_form(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse(request=request, name='auth/signup.html')


@router.post('/signup', status_code=status.HTTP_302_FOUND)
async def registrate_user(
    request: Request,
    user_registrate_schema: Annotated[UserRegistrate, Depends(register_user_form)],
    db_session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates),
):
    existing_user = await crud_user.get_single(
        db_session=db_session,
        field='email',
        value=user_registrate_schema.email,
    )
    if existing_user:
        return templates.TemplateResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            name='auth/signup.html',
            request=request,
            context={'error': f'User with email: {user_registrate_schema.email} already exists'},
        )
    user = await crud_user.create_user(db_session=db_session, user_registrate_schema=user_registrate_schema)
    request.session.clear()
    request.session['user_id'] = user.id
    return RedirectResponse(url=request.url_for('my_app_page'), status_code=status.HTTP_302_FOUND)


@router.get('/signin', response_class=HTMLResponse, name='show_signin_form')
async def show_signin_form(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    return templates.TemplateResponse(request=request, name='auth/signin.html')


@router.post('/signin', response_class=HTMLResponse)
async def signin(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(get_session),
    templates: Jinja2Templates = Depends(get_templates),
):
    user_auth_result = await authenticate_user(
        password=credentials.password,
        db_session=db_session,
        authenticate_by_field='email',
        authenticate_field_value=credentials.username,
    )
    if user_auth_result.user is None or not user_auth_result.is_authenticated:
        return templates.TemplateResponse(
            name='auth/signin.html',
            request=request,
            context={'error': 'Incorrect email or password'},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    request.session.clear()
    request.session['user_id'] = user_auth_result.user.id
    return RedirectResponse(url=request.url_for('my_app_page'), status_code=status.HTTP_302_FOUND)


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
):
    request.session.clear()
    return RedirectResponse(url=router.url_path_for('show_signin_form'), status_code=status.HTTP_302_FOUND)
