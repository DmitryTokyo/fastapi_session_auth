import pytest
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.datastructures import URL

from src.db.db_deps import get_session
from src.my_apps.users.auth.forms import register_user_form
from src.my_apps.users.crud import crud_user
from src.my_apps.users.schemas import UserRegistrate
from src.my_apps.users.tests.factories import UserFactory
from src.server import app

pytestmark = pytest.mark.asyncio


async def test_show_signup_form(client, test_server_url):
    response = client.get('/signup')
    assert response.status_code == status.HTTP_200_OK
    assert URL(f'{test_server_url}/signup') == response.url


async def test_signup_exist_user(client, test_server_url, user_factory, test_session):
    await UserFactory(username='exist username', hashed_password='hashed_password', email='test@test.com')
    user_data = UserRegistrate(
        email='test@test.com',
        password='password',
        username='exist username',
    )
    app.dependency_overrides[register_user_form] = lambda: user_data
    app.dependency_overrides[get_session] = lambda: test_session
    response = client.post('/signup', data=user_data.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.text == '{"detail":"User with email: test@test.com already exists"}'


async def test_signup_new_user(client, test_server_url, test_session):
    user_data = UserRegistrate(
        email='new@test.com',
        password='password',
        username='new username',
    )
    app.dependency_overrides[register_user_form] = lambda: user_data
    app.dependency_overrides[get_session] = lambda: test_session
    response = client.post('/signup', data=user_data.dict())
    user = await crud_user.get_by_email(db_session=test_session, email='new@test.com')
    assert response.status_code == status.HTTP_302_FOUND
    assert user is not None


async def test_show_signin_form(client, test_server_url):
    response = client.get('/signin')
    assert response.status_code == status.HTTP_200_OK
    assert URL(f'{test_server_url}/signin') == response.url


@pytest.mark.parametrize(
    'signin_email, verify_password_result, expected_status',
    [
        ('exist@test.com', True, status.HTTP_302_FOUND),
        ('exist@test.com', False, status.HTTP_401_UNAUTHORIZED),
        ('non_exist@test.com', False, status.HTTP_401_UNAUTHORIZED),
    ],
)
async def test_signin_user(
    client, test_server_url, test_session, mocker, verify_password_result, expected_status, signin_email,
):
    await UserFactory(username='exist username', hashed_password='hashed_password', email='exist@test.com')
    mocker.patch(
        'src.my_apps.users.auth.authentication.verify_password',
        return_value=verify_password_result,
    )
    oauth2_mock_form = OAuth2PasswordRequestForm(username=signin_email, password='password')
    app.dependency_overrides[OAuth2PasswordRequestForm] = lambda: oauth2_mock_form
    app.dependency_overrides[get_session] = lambda: test_session
    response = client.post('/signin', data={'username': 'exist username', 'password': 'password'})
    assert response.status_code == expected_status


async def test_logout(client, test_server_url):
    response = client.post('/logout')
    assert response.status_code == status.HTTP_302_FOUND
    assert URL(f'{test_server_url}/logout') == response.url
