from fastapi import FastAPI, Request, Depends
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from sqladmin import Admin
from starlette import status
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from src.admin.admin import AdminAuth, UserAdmin
from src.config.base import settings
from src.db.db_init import engine
from src.my_apps.app.routers import router as app_router
from src.my_apps.base_schema import CsrfSettings
from src.my_apps.users.auth.authentication import not_authenticated_exception_handler, get_current_user
from src.my_apps.users.auth.exceptions import NotAuthenticatedException
from src.my_apps.users.auth.routers import router as auth_router
from src.my_apps.users.models import User
from src.my_apps.exceptions_handler import router as exception_router
from src.my_apps.exceptions_handler import csrf_protect_exception_handler

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    ),
    Middleware(SessionMiddleware, secret_key=settings.secret_key, https_only=True),
]

app = FastAPI(openapi_url=settings.openapi_url, middleware=middlewares)
app.add_exception_handler(NotAuthenticatedException, not_authenticated_exception_handler)

app.mount('/static', StaticFiles(directory='src/my_apps/static'), name='static')

authentication_backend = AdminAuth(secret_key=settings.secret_key)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)


@app.on_event('startup')
async def startup_event():
    pass


@app.get('/', response_class=HTMLResponse)
async def base(
    request: Request,
    user: User = Depends(get_current_user),
):
    return RedirectResponse(url=request.url_for('my_app_page'), status_code=status.HTTP_302_FOUND)


@CsrfProtect.load_config
def get_csrf_config() -> CsrfSettings:
    return CsrfSettings(secret_key=settings.secret_key)


app.include_router(app_router)
app.include_router(auth_router)
app.include_router(exception_router)
app.add_exception_handler(CsrfProtectError, csrf_protect_exception_handler)

admin.add_view(UserAdmin)
