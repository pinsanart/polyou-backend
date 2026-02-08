from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta

from ..dependencies.session import get_db
from ..dependencies.auth import get_active_user
from ..core.schemas.user import UserIdentity, UserRegisterInformation

from ..infrastructure.repository.users_target_language import UsersTargetLanguagesRepositoriesSQLAlchemy
from ..services.users_sqlalchemy import UserServiceSQLAlchemy
from ..services.user_target_language import UserTargetLanguageServiceSQLAlchemy
from ..infrastructure.repository.users_sqlalchemy import UsersRepositorySQLAlchemy
from ..infrastructure.repository.languages_sqlalchemy import LanguageRepositorySQLAlchemy
from ..services.languages_sqlalchemy import LanguageServiceSQLAlchemy
from ..core.schemas.user import UserTargetLanguagesCreateInfo
from ..core.config.config import settings
from ..core.security.jwt import create_access_token
from ..core.schemas.tokens import Token

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {"description": "Not found"}}
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(db: Annotated[Session, Depends(get_db)], user_register_information: UserRegisterInformation):
    users_repository = UsersRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_service = UserServiceSQLAlchemy(users_repository, language_service)

    user_id = user_service.register(user_register_information)

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user_id}, 
        expire_delta = access_token_expire
    )
    
    return Token(access_token=access_token, token_type='bearer')

@router.post("/me/target_languages", status_code=status.HTTP_201_CREATED)
async def add_target_language_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], new_target_language_info: UserTargetLanguagesCreateInfo):
    user_id = user.user_id
    
    user_target_language_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    language_service = LanguagesServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(user_target_language_repository, language_service)

    user_target_language_service.add(user_id, new_target_language_info)
    return new_target_language_info

@router.get("/me/target_languages", status_code=status.HTTP_200_OK)
async def get_user_target_languages(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id
    
    user_target_language_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    language_service = LanguagesServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(user_target_language_repository, language_service)

    languages_iso_639_1 = user_target_language_service.list_languages_iso_639_1(user_id)
    return languages_iso_639_1

@router.get("/me", response_model=UserIdentity)
async def read_users_me(current_user: Annotated[UserIdentity, Depends(get_active_user)]):
    return current_user