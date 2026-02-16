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
    FlashcardMetadataResponse,
    FlashcardContent,
    FlashcardFSRS,
    FlashcardImage
)

from ..dependencies.sqlalchemy.factory import AppFactory
from ..dependencies.sqlalchemy.container import Container

from ..services.flashcards_sqlalchemy import FlashcardServiceSQLAlchemy
from ..services.flashcard_content_sqlalchemy import FlashcardContentServiceSQLAlchemy
from ..services.flashcard_fsrs_sqlalchemy import FlashcardFSRSServiceSQLAlchemy
from ..services.flashcard_image_sqlalchemy import FlashcardImageServiceSQLAlchemy

router = APIRouter(
    prefix="/flashcards",
    tags=['flashcards'],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=FlashcardCreateResponse)
def create_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcard_create_info: FlashcardCreateInfo):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    public_id = flashcard_service.create_one(user_id, flashcard_create_info)
    
    return FlashcardCreateResponse(
        public_id = public_id
    )

@router.post("/batch")
async def create_flashcards_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcards_create_info: List[FlashcardCreateInfo]):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    public_ids = flashcard_service.create_many(user_id, flashcards_create_info)

    return FlashcardsCreateBatchReponseModel(
        public_ids=public_ids
    )

@router.get("/")
async def get_flashcards_public_ids(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    public_ids = flashcard_service.list_public_ids(user_id)
    return {"public_ids": public_ids}

@router.delete("/")
def delete_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: Annotated[UUID, Query()]):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    flashcard_service.delete_one(user_id, public_id)

    return {"deleted_public_id": public_id}

@router.delete("/batch")
def delete_flashcard_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_ids: Annotated[List[UUID], Query()]):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    flashcard_service.delete_many(user_id, public_ids)
    
    return {"deleted_public_ids": public_ids}

@router.get("/info")
def get_flashcards_info_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_ids: Annotated[List[UUID], Query()]) -> List[FlashcardInfo]:
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    flashcards_info = flashcard_service.info(user_id, public_ids)
    return flashcards_info

@router.get("/metadata")
def get_flashcard_metadata_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID) -> FlashcardMetadataResponse:
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    metadata = flashcard_service.metadata(user_id, public_id)
    return metadata


@router.get("/all_metadata")
def get_all_flashcards_metadata_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]) -> List[FlashcardMetadataResponse]:
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    all_flashcards_metadata = flashcard_service.all_metadata(user_id)

    return all_flashcards_metadata

@router.patch("/content", response_model=FlashcardContent)
def update_flashcard_content_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_content: FlashcardContent):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_content_service = factory.create(FlashcardContentServiceSQLAlchemy)
    
    flashcard_content_service.change(user_id, public_id, new_content)

    return new_content

@router.patch("/fsrs", response_model=FlashcardFSRS)
def update_flashcard_fsrs_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_fsrs: FlashcardFSRS):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_fsrs_service = factory.create(FlashcardFSRSServiceSQLAlchemy)

    flashcard_fsrs_service.change(user_id, public_id, new_fsrs)

    return new_fsrs

@router.patch("/images", response_model=List[FlashcardImage])
def update_flashcard_images_endpoint(user: Annotated[UserIdentity, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_images: list[FlashcardImage]):
    user_id = user.user_id

    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_images_service = factory.create(FlashcardImageServiceSQLAlchemy)
    
    flashcard_images_service.update(user_id, public_id, new_images)
    return new_images