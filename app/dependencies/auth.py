from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from jwt import ExpiredSignatureError, InvalidTokenError
from ..core.exceptions.auth import UserNotFound, UserDisabled

from ..core.security.jwt import verify_token
from ..routes.auth import oauth2_scheme
from .session import get_db
from ..core.schemas.user import UserIdentity
from ..infrastructure.repository.users_sqlalchemy import UsersRepositorySQLAlchemy 
from ..core.exceptions.jwt import JWTTokenExpiredSignatureError, JWTInvalidTokenError, JWTTokenMissingSubjectError

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)])->UserIdentity:
    try:
        payload = verify_token(token)
    except ExpiredSignatureError:
        raise JWTTokenExpiredSignatureError("The access token is expired.")
    except InvalidTokenError:
        raise JWTInvalidTokenError("The access token is invalid.")
     
    user_id = payload.get('sub')
    
    if not user_id:
        raise JWTTokenMissingSubjectError("The token has no subject (sub).")    
    
    user_repository = UsersRepositorySQLAlchemy(db)
    
    user = user_repository.get_by_id(user_id)
    
    if not user:
        raise UserNotFound(f"The user_id {user_id} was not found in the database.")
    
    return UserIdentity(
        user_id= user.user_id,
        disabled= user.disabled
    )

def get_active_user(current_user: Annotated[UserIdentity, Depends(get_current_user)]) -> UserIdentity:
    if current_user.disabled:
        raise UserDisabled(f"The user_id {current_user.user_id} is disabled.")
    return current_user