from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False


class UserCreateDB(UserBase):
    hashed_password: str


class UserRegistrate(UserBase):
    password: str


class UserUpdateDB(UserBase):
    password: str = Field(default=None)
    email: EmailStr = Field(default=None)
    username: str = Field(default=None)
    is_staff: bool = Field(default=False)


class UserOutDB(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
