from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.templating import Jinja2Templates

from src.dependencies import get_templates
from src.my_apps.users.auth.authentication import get_current_user
from src.my_apps.users.models import User

router = APIRouter(tags=['app'])


@router.get('/app', response_class=HTMLResponse)
async def my_app_page(
    request: Request, response: Response,
    templates: Jinja2Templates = Depends(get_templates),
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(request=request, name='app/app.html')
