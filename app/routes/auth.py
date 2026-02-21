from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta

from ..core.security.jwt import create_access_token 
from ..core.schemas.tokens.tokens import Token
from ..core.schemas.users.requests import UserLoginRequest
from ..services.sqlalchemy.auth.auth import AuthServiceSQLAlchemy
from ..core.config.config import settings

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.factory import AppFactory
from ..dependencies.sqlalchemy.container import Container

router = APIRouter(
    prefix="/auth",
    tags=['auth'],
    responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/token", tags=['auth'])
def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]) -> Token:
    container = Container(db)
    factory = AppFactory(container)

    auth_service = factory.create(AuthServiceSQLAlchemy)
    
    user_login_credentials = UserLoginRequest(
        email=form_data.username,
        password=form_data.password
    )

    user_id = auth_service.authenticate_user(user_login_credentials)

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": str(user_id)}, 
        expire_delta = access_token_expire
    )
    
    return Token(access_token=access_token, token_type='bearer')