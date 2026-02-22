from fastapi import APIRouter, Depends, Query, Body
from typing import Annotated, List
from sqlalchemy.orm import Session
from uuid import UUID

from ..services.sqlalchemy.flashcards.flashcard import FlashcardServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_content import FlashcardContentServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_metadata import FlashcardMetadataServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_fsrs import FlashcardFSRSServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_image import FlashcadImageServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_review import FlashcardReviewServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_audio import FlashcardAudioServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_metadata import FlashcardMetadataServiceSQLAlchemy

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.auth.auth import get_active_user

from ..core.schemas.users.responses import UserIdentityResponse

from ..core.schemas.flashcards.responses import (
    FlashcardCreateResponse,
    FlashcardCreateBatchResponse,
    UserFlashcardsPublicIdsResponse,
    FlashcardDeleteResponse,
    FlashcardDeleteBatchResponse,
    FlashcardInfoResponse,
    FlashcardChangeContentResponse,
    FlashcardMetadataResponse,
    FlaschardAllMetadataResponse,
    FlashcardChangeFSRSResponse,
    FlashcardChangeImagesResponse,
    FlashcardChangeReviewsResponse,
    FlashcardChangeAudiosResponse,
    FlashcardChangeMetadataResponse
)

from ..core.schemas.flashcards.requests import (
    FlashcardCreateRequest,
    FlashcardContentRequest,
    FlashcardFSRSRequest,
    FlashcardImageRequest,
    FlashcardReviewRequest,
    FlashcardAudioRequest,
    FlashcardMetadataRequest
)

from ..dependencies.sqlalchemy.factory import AppFactory
from ..dependencies.sqlalchemy.container import Container

from ..mappers.flashcard_request import FlashcardRequestMapper
from ..mappers.flashcard_response import FlashcardResponseMapper

router = APIRouter(
    prefix="/flashcards",
    tags=['flashcards'],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=UserFlashcardsPublicIdsResponse)
async def get_flashcards_public_ids(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    public_ids = flashcard_service.list_public_ids(user_id)
    return UserFlashcardsPublicIdsResponse(public_ids=public_ids)

@router.get("/info", response_model=List[FlashcardInfoResponse])
def get_flashcards_info(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_ids: Annotated[List[UUID], Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcards_ids = flashcard_service.get_ids_by_public_ids_or_fail(user_id, public_ids)

    infos = flashcard_service.info_many(flashcards_ids)

    flashcard_response_mapper = factory.create(FlashcardResponseMapper)
    return [flashcard_response_mapper.model_to_response(info) for info in infos]

@router.get("/metadata", response_model=FlashcardMetadataResponse)
def get_flashcard_metadata(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service:FlashcardServiceSQLAlchemy = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_metadata_service:FlashcardMetadataServiceSQLAlchemy = factory.create(FlashcardMetadataServiceSQLAlchemy)
    metadata = flashcard_metadata_service.info_one(flashcard_id)

    flashcard_response_mapper:FlashcardResponseMapper = factory.create(FlashcardResponseMapper)
    return flashcard_response_mapper.metadata_to_response(user_id, metadata)

@router.get("/all_metadata", response_model=FlaschardAllMetadataResponse)
def get_all_flashcards_metadata(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_metadata_service:FlashcardMetadataServiceSQLAlchemy = factory.create(FlashcardMetadataServiceSQLAlchemy)
    metadatas = flashcard_metadata_service.info_all(user_id)

    flashcard_response_mapper:FlashcardResponseMapper = factory.create(FlashcardResponseMapper)
    return flashcard_response_mapper.all_metadata_to_response(user_id, metadatas)

@router.post("/", response_model=FlashcardCreateResponse)
def create_flashcard(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcard_create_info: FlashcardCreateRequest):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_request_mapper = factory.create(FlashcardRequestMapper)

    create_info = flashcard_request_mapper.request_to_create(flashcard_create_info)
    public_id = flashcard_service.create_one(user_id, create_info)
    
    return FlashcardCreateResponse(public_id=public_id)

@router.post("/batch", response_model=FlashcardCreateBatchResponse)
async def create_flashcards(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], flashcards_create_info: Annotated[List[FlashcardCreateRequest], Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_request_mapper = factory.create(FlashcardRequestMapper)
    
    create_infos = [flashcard_request_mapper.request_to_create(create_info) for create_info in flashcards_create_info]
    public_ids = flashcard_service.create_many(user_id, create_infos)

    return FlashcardCreateBatchResponse(public_ids=public_ids)
         
@router.patch("/content", response_model=FlashcardChangeContentResponse)
def update_flashcard_content(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_content: FlashcardContentRequest):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_content_service = factory.create(FlashcardContentServiceSQLAlchemy)
    flashcard_content_service.change(flashcard_id, new_content) 

    return FlashcardChangeContentResponse(public_id=public_id, new_content=new_content)
    
@router.patch("/fsrs", response_model=FlashcardChangeFSRSResponse)
def update_flashcard_fsrs(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_fsrs: FlashcardFSRSRequest):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_fsrs_service:FlashcardFSRSServiceSQLAlchemy = factory.create(FlashcardFSRSServiceSQLAlchemy)
    flashcard_fsrs_service.change(flashcard_id, new_fsrs)

    return FlashcardChangeFSRSResponse(public_id=public_id, new_fsrs=new_fsrs)

@router.patch("/images", response_model=FlashcardChangeImagesResponse)
def update_flashcard_images(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_images: Annotated[List[FlashcardImageRequest], Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_image_service = factory.create(FlashcadImageServiceSQLAlchemy)
    flashcard_image_service.change(flashcard_id, new_images)

    return FlashcardChangeImagesResponse(public_id=public_id, new_images=new_images)

@router.patch("/reviews", response_model=FlashcardChangeReviewsResponse)
def update_flashcard_reviews(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_reviews: Annotated[List[FlashcardReviewRequest], Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_review_service= factory.create(FlashcardReviewServiceSQLAlchemy)
    flashcard_review_service.change(flashcard_id, new_reviews)

    return FlashcardChangeReviewsResponse(public_id=public_id, new_reviews=new_reviews)

@router.patch("/audios", response_model=FlashcardChangeAudiosResponse)
def update_flashcard_audio(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_audios: Annotated[List[FlashcardAudioRequest], Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_audio_service = factory.create(FlashcardAudioServiceSQLAlchemy)
    flashcard_audio_service.change(flashcard_id, new_audios)

    return FlashcardChangeAudiosResponse(public_id=public_id, new_audios=new_audios)

@router.patch("/metadata", response_model=FlashcardChangeMetadataResponse)
def update_flashcard_metadata(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID, new_metadata: FlashcardMetadataRequest):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)

    flashcard_metadata_service = factory.create(FlashcardMetadataServiceSQLAlchemy)
    flashcard_metadata_service.change(flashcard_id, new_metadata)

    return FlashcardChangeMetadataResponse(public_id=public_id, new_metadata=new_metadata)


@router.delete("/", response_model=FlashcardDeleteResponse)
def delete_flashcard(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_id: UUID):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service= factory.create(FlashcardServiceSQLAlchemy)
    
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, public_id)
    flashcard_service.delete_one(flashcard_id)

    return FlashcardDeleteResponse(deleted_public_id=public_id)

@router.delete("/batch", response_model=FlashcardDeleteBatchResponse)
def delete_flashcards(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], public_ids: Annotated[List[UUID], Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcards_ids = flashcard_service.get_ids_by_public_ids_or_fail(user_id, public_ids)
    
    flashcard_service.delete_many(flashcards_ids)

    return FlashcardDeleteBatchResponse(deleted_public_ids=public_ids)