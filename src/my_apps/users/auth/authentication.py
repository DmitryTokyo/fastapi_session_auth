from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.db.db_deps import get_session
from src.my_apps.users.auth.custom_types import AuthenticationResult
from src.my_apps.users.auth.exceptions import NotAuthenticatedException

from src.my_apps.users.auth.passwords import verify_password
from src.my_apps.users.crud import crud_user
from src.my_apps.users.models import User


async def authenticate_user(db_session: AsyncSession, credentials: OAuth2PasswordRequestForm) -> AuthenticationResult:
    user = await crud_user.get_by_email(db_session=db_session, email=credentials.username)
    if not user:
        return AuthenticationResult(user=None, is_authenticated=False)
    if not verify_password(credentials.password, user.hashed_password):
        return AuthenticationResult(user=None, is_authenticated=False)

    return AuthenticationResult(user=user, is_authenticated=True)


async def get_current_user(request: Request, db_session: AsyncSession = Depends(get_session)) -> User | None:
    user_id = request.session.get('user_id')
    if user_id is None:
        raise NotAuthenticatedException(status_code=status.HTTP_403_FORBIDDEN)
    user = await crud_user.get_single(db_session=db_session, obj_id=user_id)
    if user is None:
        raise NotAuthenticatedException(status_code=status.HTTP_403_FORBIDDEN)
    return user


async def not_authenticated_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url=request.url_for('show_signin_form'), status_code=status.HTTP_302_FOUND)
