from fastapi import APIRouter, Depends, Query
from typing import Annotated, List
from sqlalchemy.orm import Session
from uuid import UUID

from ..dependencies.session import get_db
from ..dependencies.auth import get_active_user

from ..core.schemas.user import UserIdentity
from ..core.schemas.flashcards import (
    FlashcardCreateInfo, 
    FlashcardCreateResponse, 
    FlashcardsCreateBatchReponseModel,
    FlashcardInfo,
    FlashcardMetadataResponse
)

from ..services.flashcards_sqlalchemy import FlashcardServiceSQLAlchemy
from ..services.user_target_language import UserTargetLanguageServiceSQLAlchemy
from ..services.languages_sqlalchemy import LanguageServiceSQLAlchemy
from ..services.flascards_types_sqlalchemy import FlashcardsTypesServiceSQLAlchemy
from ..infrastructure.repository.flashcards_type_sqlalchemy import FlashcardTypesRepositorySQLAlchemy
from ..infrastructure.repository.flashcards_sqlalchemy import FlashcardRepositorySQLAlchemy
from ..infrastructure.repository.users_target_language import UsersTargetLanguagesRepositoriesSQLAlchemy
from ..infrastructure.repository.languages_sqlalchemy import LanguageRepositorySQLAlchemy

router = APIRouter(
    prefix="/flashcards",
    tags=['flashcards'],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=FlashcardCreateResponse)
def create_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcard_create_info: FlashcardCreateInfo):
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    public_id = flashcard_service.create_one(user_id, flashcard_create_info)
    
    return FlashcardCreateResponse(
        public_id = public_id
    )

@router.post("/batch")
async def create_flashcards_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcards_create_info: List[FlashcardCreateInfo]):
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)
    public_ids = flashcard_service.create_many(user_id, flashcards_create_info)

    return FlashcardsCreateBatchReponseModel(
        public_ids=public_ids
    )

@router.get("/")
async def get_flashcards_public_ids(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    public_ids = flashcard_service.list_public_ids(user_id)
    return {"public_ids": public_ids}

@router.delete("/")
def delete_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: Annotated[UUID, Query()]):
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    flashcard_service.delete_one(user_id, public_id)

    return {"deleted_public_id": public_id}

@router.delete("/batch")
def delete_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_ids: Annotated[List[UUID], Query()]):
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    flashcard_service.delete_many(user_id, public_ids)
    
    return {"deleted_public_ids": public_ids}

@router.get("/info")
def get_flashcards_info_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_ids: Annotated[List[UUID], Query()]) -> List[FlashcardInfo]:
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    flashcards_info = flashcard_service.info(user_id, public_ids)
    return flashcards_info

@router.get("/metadata")
def get_flashcard_metadata_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID) -> FlashcardMetadataResponse:
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    metadata = flashcard_service.metadata(user_id, public_id)
    return metadata


@router.get("/all_metadata")
def get_all_flashcards_metadata_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]) -> List[FlashcardMetadataResponse]:
    user_id = user.user_id

    flashcards_repository = FlashcardRepositorySQLAlchemy(db)
    languages_repository = LanguageRepositorySQLAlchemy(db)
    users_target_languages_repository = UsersTargetLanguagesRepositoriesSQLAlchemy(db)
    flashcards_types_repository = FlashcardTypesRepositorySQLAlchemy(db)

    flashcard_type_service = FlashcardsTypesServiceSQLAlchemy(flashcards_types_repository)
    language_service = LanguageServiceSQLAlchemy(languages_repository)
    user_target_language_service = UserTargetLanguageServiceSQLAlchemy(users_target_languages_repository, language_service)
    flashcard_service = FlashcardServiceSQLAlchemy(flashcards_repository, user_target_language_service, flashcard_type_service, language_service)

    all_flashcards_metadata = flashcard_service.all_metadata(user_id)

    return all_flashcards_metadata