from typing import NamedTuple

from src.my_apps.users.models import User


class AuthenticationResult(NamedTuple):
    user: User | None
    is_authenticated: bool
