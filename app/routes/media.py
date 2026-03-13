from fastapi import APIRouter, UploadFile, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.auth.auth import get_active_user
from ..core.schemas.users.responses import UserIdentityResponse

from ..dependencies.sqlalchemy.factory import AppFactory
from ..dependencies.sqlalchemy.container import Container
from ..services.sqlalchemy.users.user import UserServiceSQLAlchemy

router = APIRouter(
    prefix="/media",
    tags=['media'],
    responses={404: {"description": "Not found"}}
)

@router.post('/')
def upload_midia_file(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], file: UploadFile):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    user_service:UserServiceSQLAlchemy = factory.create(UserServiceSQLAlchemy)
    
    user_public_id = user_service.get_public_id_or_fail(user_id)

    