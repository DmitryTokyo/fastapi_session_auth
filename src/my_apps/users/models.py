from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.db.db_init import Base


class User(Base):
    __tablename__ = 'app_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(200))
    hashed_password: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return self.username

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            return self.id == other.id
        return False
