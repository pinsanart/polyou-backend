from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.auth.auth import get_active_user

from ..core.config.config import settings
from ..core.security.jwt import create_access_token
from ..core.schemas.tokens.tokens import Token

from ..dependencies.sqlalchemy.container import Container
from ..dependencies.sqlalchemy.factory import AppFactory

from ..services.sqlalchemy.users.user import UserServiceSQLAlchemy
from ..services.sqlalchemy.users.user_target_language import UserTargetLanguageServiceSQLAlchemy
from ..services.sqlalchemy.languages.language import LanguageServiceSQLAlchemy

from ..core.schemas.users.creates import UserCreateInfo
from ..core.schemas.users.responses import UserIdentityResponse, UserTargetLanguageResponse, UserTargetLanguageCreateResponse
from ..core.schemas.users.creates import UserTargetLanguageCreateInfo
from ..core.schemas.users.requests import UserTargetLanguageCreateRequest

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {"description": "Not found"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Token)
async def create_user(db: Annotated[Session, Depends(get_db)], user_register_information: Annotated[UserCreateInfo, Body()]):
    container = Container(db)
    factory = AppFactory(container)

    user_service = factory.create(UserServiceSQLAlchemy)

    user_id = user_service.register(user_register_information)

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user_id}, 
        expire_delta = access_token_expire
    )
    
    return Token(access_token=access_token, token_type='bearer')

@router.post("/me/target_languages", status_code=status.HTTP_201_CREATED, response_model=UserTargetLanguageCreateResponse)
async def add_target_language(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], new_target_language_info: Annotated[UserTargetLanguageCreateRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    language_service = factory.create(LanguageServiceSQLAlchemy)
    user_target_language_service = factory.create(UserTargetLanguageServiceSQLAlchemy)

    language_id = language_service.get_id_by_iso_639_1_or_fail(new_target_language_info.iso_639_1)

    create_info = UserTargetLanguageCreateInfo(
        user_id=user_id,
        language_id= language_id
    )

    user_target_language_service.add(user_id, create_info)
    return UserTargetLanguageCreateResponse(created_target_language = new_target_language_info.iso_639_1)

@router.get("/me/target_languages", response_model=UserTargetLanguageResponse)
async def get_user_target_languages(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)

    language_service = factory.create(LanguageServiceSQLAlchemy)
    user_target_language_service = factory.create(UserTargetLanguageServiceSQLAlchemy)
    
    language_ids = user_target_language_service.list_user_languages_ids(user_id)
    languages_iso_639_1 = [language_service.get_iso_639_1_by_id_or_fail(id) for id in language_ids]
    
    return UserTargetLanguageResponse(user_target_languages=languages_iso_639_1)
    
@router.get("/me", response_model=UserIdentityResponse)
async def read_users_me(current_user: Annotated[UserIdentityResponse, Depends(get_active_user)]):
    return current_user