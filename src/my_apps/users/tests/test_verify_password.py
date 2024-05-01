import bcrypt
import pytest

from src.my_apps.users.auth.passwords import verify_password


@pytest.mark.parametrize(
    'test_password, expected',
    [
        ('secure_password', True),
        ('wrong_password', False),
    ],
)
def test_verify_password(test_password, expected):
    secure_decoded_password = 'secure_password'.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=secure_decoded_password, salt=salt)
    assert verify_password(test_password, hashed_password.decode()) == expected
