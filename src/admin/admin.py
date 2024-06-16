from datetime import datetime, timezone, timedelta

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
import jwt

from src.config.base import settings
from src.db.db_deps import get_session
from src.my_apps.users.auth.authentication import authenticate_user
from src.my_apps.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.is_active, User.is_superuser, User.is_staff]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form['username'], form['password']
        session_generator = get_session()
        db_session = await anext(session_generator)
        user_auth_result = await authenticate_user(
            password=password,
            db_session=db_session,
            authenticate_by_field='username',
            authenticate_field_value=username,
        )
        if not user_auth_result.is_authenticated or not user_auth_result.user.is_superuser:
            return False

        admin_jwt_token = _generate_admin_jwt_token(user_id=user_auth_result.user.id)
        request.session.update({'admin_token': admin_jwt_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.pop('admin_token', None)
        return True

    async def authenticate(self, request: Request) -> bool:
        admin_token = request.session.get('admin_token')
        user_id = request.session.get('user_id')
        if not user_id:
            return False
        try:
            jwt.decode(admin_token, settings.secret_key, algorithms=settings.hash_algorithm)
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            return False
        admin_jwt_token = _generate_admin_jwt_token(user_id=user_id)
        request.session.update({'admin_token': admin_jwt_token})
        return True


def _generate_admin_jwt_token(user_id: int) -> str:
    expiration_datetime = (
        datetime.now(tz=timezone.utc) + timedelta(seconds=settings.admin_session_expiration_seconds)
    )
    admin_jwt_token = jwt.encode(
        {'admin_user_id': user_id, 'exp': expiration_datetime},
        settings.secret_key,
        algorithm=settings.hash_algorithm,
    )
    return admin_jwt_token
