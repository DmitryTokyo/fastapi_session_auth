from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from src.config.base import settings
from src.db.db_deps import get_session
from src.my_apps.users.models import User


def get_templates() -> Jinja2Templates:
    return Jinja2Templates(directory=settings.TEMPLATES_ROOT)


def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User | None:
    user_id = request.session.get('user_id')
    if user_id is None:
        raise HTTPException(status_code=400, detail='Not authenticated')
    return session.query(User).filter(User.id == user_id).first()
