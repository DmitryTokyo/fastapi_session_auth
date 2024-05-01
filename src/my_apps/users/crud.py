from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_apps.base_crud import CRUDBase
from src.my_apps.users.auth.passwords import get_password_hash
from src.my_apps.users.models import User
from src.my_apps.users.schemas import UserCreateDB, UserUpdateDB, UserOutDB, UserRegistrate


class CRUDUser(CRUDBase[UserCreateDB, UserUpdateDB, UserOutDB]):

    async def create_user(self, db_session: AsyncSession, user_registrate_schema: UserRegistrate) -> User:
        user_registrate_schema_dict = user_registrate_schema.dict()
        user_registrate_schema_dict['hashed_password'] = get_password_hash(user_registrate_schema_dict.pop('password'))
        user_create_schema = UserCreateDB(**user_registrate_schema_dict)
        return await self.create(db_session=db_session, schema_in=user_create_schema)

    async def get_by_email(self, db_session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        db_execution = await db_session.execute(stmt)
        return db_execution.scalar_one_or_none()


crud_user = CRUDUser(User)
