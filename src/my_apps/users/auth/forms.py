from fastapi import Form
from pydantic import EmailStr

from src.my_apps.users.schemas import UserRegistrate


async def register_user_form(
    username: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
) -> UserRegistrate:
    return UserRegistrate(email=email, password=password, username=username)
