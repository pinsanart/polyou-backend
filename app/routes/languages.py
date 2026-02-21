from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.container import Container
from ..dependencies.sqlalchemy.factory import AppFactory

from ..core.schemas.languages.responses import AvailableLanguageResponse
from ..services.sqlalchemy.languages.language import LanguageServiceSQLAlchemy

router = APIRouter(
    prefix="/languages",
    tags=['languages'],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=AvailableLanguageResponse)
def get_available_languages(db:Annotated[Session, Depends(get_db)]):
    container = Container(db)
    factory = AppFactory(container)

    language_service:LanguageServiceSQLAlchemy = factory.create(LanguageServiceSQLAlchemy)

    languages_iso_639_1 = language_service.get_available_languages_iso_639_1()
    return AvailableLanguageResponse(available_languages=languages_iso_639_1)