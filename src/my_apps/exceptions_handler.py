from fastapi import Depends, APIRouter
from fastapi_csrf_protect.exceptions import CsrfProtectError
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from src.dependencies import get_templates

router = APIRouter(tags=['exception'])


@router.get('/forbidden', response_class=HTMLResponse)
async def show_forbidden_page(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
):
    return templates.TemplateResponse(request=request, name='exceptions/403_forbidden.html')


async def csrf_protect_exception_handler(
    request: Request,
    exc: CsrfProtectError,
):
    redirect_url = str(request.url_for('show_forbidden_page'))
    if 'HX-Request' in request.headers:
        return JSONResponse(
            {'location': redirect_url},
            status_code=status.HTTP_200_OK,
            headers={'HX-Redirect': redirect_url},
        )
    else:
        return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
