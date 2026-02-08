from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..services.languages_sqlalchemy import LanguageServiceSQLAlchemy
from ..infrastructure.repository.languages_sqlalchemy import LanguageRepositorySQLAlchemy
from ..dependencies.session import get_db

router = APIRouter(
    prefix="/languages",
    tags=['languages'],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=list[str])
def get_available_language_endpoint(db:Annotated[Session, Depends(get_db)]):
    languages_repository = LanguageRepositorySQLAlchemy(db)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    return language_service.get_available()