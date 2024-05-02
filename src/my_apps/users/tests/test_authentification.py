import pytest
from fastapi.security import OAuth2PasswordRequestForm

from src.my_apps.users.auth.authentication import authenticate_user
from src.my_apps.users.auth.custom_types import AuthenticationResult
from src.my_apps.users.tests.factories import UserFactory

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'verify_password_result, is_authenticated_expected, is_user_expected',
    [
        (True, True, True),
        (False, False, False),
    ],
)
async def test_authenticate_user(
    test_session, mocker, verify_password_result, is_authenticated_expected, is_user_expected,
):
    mocker.patch('src.my_apps.users.auth.authentication.verify_password', return_value=verify_password_result)
    user = await UserFactory(username='auth user', hashed_password='hashed_password', email='test@test.com')
    credentials = OAuth2PasswordRequestForm(username='test@test.com', password='password')
    expected = AuthenticationResult(
        user=user if is_user_expected else None,
        is_authenticated=is_authenticated_expected,
    )
    auth_result = await authenticate_user(db_session=test_session, credentials=credentials)
    assert auth_result == expected
