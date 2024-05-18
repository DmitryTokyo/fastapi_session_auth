from datetime import datetime

from fastapi import APIRouter, Depends, Form
from fastapi_csrf_protect import CsrfProtect
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.dependencies import get_templates
from src.my_apps.users.auth.authentication import get_current_user
from src.my_apps.users.models import User

router = APIRouter(tags=['app'])


@router.get('/app', response_class=HTMLResponse)
async def my_app_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    user: User = Depends(get_current_user),
    csrf_protect: CsrfProtect = Depends(),
):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = templates.TemplateResponse(request=request, name='app/app.html', context={'csrf_token': csrf_token})
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post('/app', response_class=HTMLResponse)
async def load_form_data(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    user: User = Depends(get_current_user),
    csrf_protect: CsrfProtect = Depends(),
    selection: str = Form(...),
):
    await csrf_protect.validate_csrf(request)
    result_data = {
        'datetime': datetime.now().strftime('%Y-%m-%D %H:%M:%S'),
        'result': selection,
    }
    response = templates.TemplateResponse(
        request=request,
        name='app/submission_results.html',
        context={'result_data': result_data},
    )
    return response
