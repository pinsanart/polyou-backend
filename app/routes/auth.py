from fastapi import Depends, Form, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from ..services.sqlalchemy.auth.auth import AuthServiceSQLAlchemy
from ..services.sqlalchemy.auth.refresh_token import RefreshTokenServiceSQLAlchemy

from ..core.security.jwt import create_access_token
from ..core.config.config import settings

from ..core.schemas.auth.create import RefreshTokenCreateInfo
from ..core.schemas.auth.request import DeviceInfoRequest, LoginRequest
from ..core.schemas.auth.response import TokenResponse

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.factory import AppFactory
from ..dependencies.sqlalchemy.container import Container

router = APIRouter(
    prefix="/auth",
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", response_model=TokenResponse)
def login_access_token(
    login_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
    request: Request,
    device_id: Annotated[UUID | None, Form()] = None,
    device_name: Annotated[str | None, Form()] = None,
):
    if device_id is None:
        device_id = '00000000-0000-0000-0000-000000000000'

    if device_name is None:
        device_name = "Swagger UI"

    container = Container(db)
    factory = AppFactory(container)

    auth_service = factory.create(AuthServiceSQLAlchemy)
    user_refresh_token_service = factory.create(RefreshTokenServiceSQLAlchemy)

    login_data = LoginRequest(
        email=login_credentials.username,
        password=login_credentials.password
    )

    user_id = auth_service.authenticate_user(login_data)

    access_token = create_access_token(
        data={"sub": str(user_id)},
        expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = user_refresh_token_service.create(
        user_id=user_id,
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        user_refresh_token_info=RefreshTokenCreateInfo(
            device_id=device_id,
            device_name=device_name,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )