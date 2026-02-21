from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from jwt import ExpiredSignatureError, InvalidTokenError
from ....core.exceptions.auth import UserNotFound, UserDisabled

from ....core.security.jwt import verify_token
from ....routes.auth import oauth2_scheme
from ...session import get_db
from ....core.schemas.users.responses import UserIdentityResponse
from ....infrastructure.repository.sqlalchemy.users.user_metadata import UserMetadataRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user import UserRepositorySQLAlchemy 
from ....core.exceptions.jwt import JWTTokenExpiredSignatureError, JWTInvalidTokenError, JWTTokenMissingSubjectError

from ....dependencies.sqlalchemy.container import Container
from ....dependencies.sqlalchemy.factory import AppFactory

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]) -> UserIdentityResponse:
    try:
        payload = verify_token(token)
    except ExpiredSignatureError:
        raise JWTTokenExpiredSignatureError("The access token is expired.")
    except InvalidTokenError:
        raise JWTInvalidTokenError("The access token is invalid.")
     
    user_id = payload.get('sub')

    if not user_id:
        raise JWTTokenMissingSubjectError("The token has no subject (sub).")    
    
    container = Container(db)
    factory = AppFactory(container)
    
    user_repository = factory.create(UserRepositorySQLAlchemy)
    
    user_model = user_repository.get_by_id(user_id)
    
    if not user_model:
        raise UserNotFound(f"User id={user_id} not found.")
    
    user_metadata_repository = factory.create(UserMetadataRepositorySQLAlchemy)
    user_metadata_model = user_metadata_repository.get(user_id)
    
    return UserIdentityResponse(
        user_id= user_model.user_id,
        disabled= user_metadata_model.disabled
    )

def get_active_user(current_user: Annotated[UserIdentityResponse, Depends(get_current_user)]) -> UserIdentityResponse:
    if current_user.disabled:
        raise UserDisabled(f"The user_id {current_user.user_id} is disabled.")
    return current_user