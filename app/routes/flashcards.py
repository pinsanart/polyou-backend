from fastapi import APIRouter, Depends, Query, Body
from typing import Annotated, List
from sqlalchemy.orm import Session
from uuid import UUID

from ..services.sqlalchemy.flashcards.flashcard import FlashcardServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_content import FlashcardContentServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_sync_metadata import FlashcardSyncMetadataServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_fsrs import FlashcardFSRSServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_image import FlashcadImageServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_review import FlashcardReviewServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_audio import FlashcardAudioServiceSQLAlchemy
from ..services.sqlalchemy.flashcards.flashcard_sync_metadata import FlashcardSyncMetadataServiceSQLAlchemy

from ..dependencies.session import get_db
from ..dependencies.sqlalchemy.auth.auth import get_active_user

from ..core.schemas.users.responses import UserIdentityResponse

from ..core.schemas.flashcards.requests import (
    FlashcardPostRequest,
    FlashcardPatchContentRequest,
    FlashcardPatchFSRSRequest,
    FlashcardPatchImagesRequest,
    FlashcardPatchReviewsRequest,
    FlashcardPatchAudiosRequest,
    FlashcardPatchSyncMetadataRequest,
    FlashcardGetInfoRequest,
    FlashcardGetSyncMetadataRequest,
    FlashcardPostBatchRequest,
    FlashcardDeleteRequest,
    FlashcardDeleteBatchRequest
)

from ..core.schemas.flashcards.responses import (
    FlashcardGetResponse,
    FlashcardGetInfosResponse,
    FlashcardGetSyncMetadataResponse,
    FlashcardGetAllSyncMetadataResponse,
    FlashcardPostResponse,
    FlashcardPostBatchResponse,
    FlashcardPatchContentResponse,
    FlashcardPatchFSRSResponse,
    FlaschardPatchImagesResponse,
    FlashcardPatchReviewsResponse,
    FlashcardPatchAudiosResponse,
    FlashcardPatchSyncMetadataResponse,
    FlashcardDeleteResponse,
    FlashcardDeleteBatchResponse
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

@router.get("/", response_model=FlashcardGetResponse)
async def get_flashcards_public_ids(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)

    public_ids = flashcard_service.list_public_ids(user_id)
    return FlashcardGetResponse(public_ids=public_ids)

@router.get("/infos", response_model=FlashcardGetInfosResponse)
def get_flashcards_info(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardGetInfoRequest, Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcards_ids = flashcard_service.get_ids_by_public_ids_or_fail(user_id, request.public_ids)

    infos = flashcard_service.info_many(flashcards_ids)

    flashcard_response_mapper = factory.create(FlashcardResponseMapper)
    infos = [flashcard_response_mapper.model_to_response(info) for info in infos]
    
    return FlashcardGetInfosResponse(
        infos=infos
    )

@router.get("/sync_metadata", response_model=FlashcardGetSyncMetadataResponse)
def get_flashcard_metadata(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardGetSyncMetadataRequest, Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service:FlashcardServiceSQLAlchemy = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_metadata_service = factory.create(FlashcardSyncMetadataServiceSQLAlchemy)
    metadata = flashcard_metadata_service.info_one(flashcard_id)

    flashcard_response_mapper:FlashcardResponseMapper = factory.create(FlashcardResponseMapper)
    return flashcard_response_mapper.sync_metadata_to_response(user_id, metadata)

@router.get("/all_sync_metadata", response_model=FlashcardGetAllSyncMetadataResponse)
def get_all_flashcards_metadata(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)
    
    flashcard_metadata_service = factory.create(FlashcardSyncMetadataServiceSQLAlchemy)
    metadatas = flashcard_metadata_service.info_all(user_id)

    flashcard_response_mapper:FlashcardResponseMapper = factory.create(FlashcardResponseMapper)
    return flashcard_response_mapper.all_sync_metadata_to_response(user_id, metadatas)

@router.post("/", response_model=FlashcardPostResponse)
def create_flashcard(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPostRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service:FlashcardServiceSQLAlchemy = factory.create(FlashcardServiceSQLAlchemy)
    
    public_id = flashcard_service.create_one_from_request(user_id, request)
    
    return FlashcardPostResponse(
        public_id=public_id
    )

@router.post("/batch", response_model=FlashcardPostBatchResponse)
async def create_flashcards(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPostBatchRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_request_mapper = factory.create(FlashcardRequestMapper)
    
    create_infos = [flashcard_request_mapper.request_to_create(create_info) for create_info in request.flashcards]
    public_ids = flashcard_service.create_many(user_id, create_infos)

    return FlashcardPostBatchResponse(public_ids=public_ids)
         
@router.patch("/content", response_model=FlashcardPatchContentResponse)
def update_flashcard_content(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPatchContentRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_content_service = factory.create(FlashcardContentServiceSQLAlchemy)
    flashcard_content_service.change(flashcard_id, request.new_content) 

    return FlashcardPatchContentResponse(
        public_id=request.public_id, 
        new_content=request.new_content
    )
    
@router.patch("/fsrs", response_model=FlashcardPatchFSRSResponse)
def update_flashcard_fsrs(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPatchFSRSRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_fsrs_service:FlashcardFSRSServiceSQLAlchemy = factory.create(FlashcardFSRSServiceSQLAlchemy)
    flashcard_fsrs_service.change(flashcard_id, request.new_fsrs)

    return FlashcardPatchFSRSResponse(
        public_id=request.public_id, 
        new_fsrs=request.new_fsrs
    )

@router.patch("/images", response_model=FlaschardPatchImagesResponse)
def update_flashcard_images(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPatchImagesRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_image_service = factory.create(FlashcadImageServiceSQLAlchemy)
    flashcard_image_service.change(flashcard_id, request.new_images)

    return FlaschardPatchImagesResponse(
        public_id=request.public_id, 
        new_images=request.new_images
    )

@router.patch("/reviews", response_model=FlashcardPatchReviewsResponse)
def update_flashcard_reviews(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPatchReviewsRequest, Body()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_review_service= factory.create(FlashcardReviewServiceSQLAlchemy)
    flashcard_review_service.change(flashcard_id, request.new_reviews)

    return FlashcardPatchReviewsResponse(
        public_id=request.public_id, 
        new_reviews=request.new_reviews
    )

@router.patch("/audios", response_model=FlashcardPatchAudiosResponse)
def update_flashcard_audio(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPatchAudiosRequest, Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_audio_service = factory.create(FlashcardAudioServiceSQLAlchemy)
    flashcard_audio_service.change(flashcard_id, request.new_audios)

    return FlashcardPatchAudiosResponse(
        public_id=request.public_id, 
        new_audios=request.new_audios
    )

@router.patch("/sync_metadata", response_model=FlashcardPatchSyncMetadataResponse)
def update_flashcard_metadata(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardPatchSyncMetadataRequest, Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)

    flashcard_metadata_service = factory.create(FlashcardSyncMetadataServiceSQLAlchemy)
    flashcard_metadata_service.change(flashcard_id, request.new_sync_metadata)

    return FlashcardPatchSyncMetadataResponse(
        public_id=request.public_id, 
        new_metadata=request.new_sync_metadata
    )

@router.delete("/", response_model=FlashcardDeleteResponse)
def delete_flashcard(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardDeleteRequest, Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service= factory.create(FlashcardServiceSQLAlchemy)
    
    flashcard_id = flashcard_service.get_id_by_public_id_or_fail(user_id, request.public_id)
    flashcard_service.delete_one(flashcard_id)

    return FlashcardDeleteResponse(
        deleted_public_id=request.public_id
    )

@router.delete("/batch", response_model=FlashcardDeleteBatchResponse)
def delete_flashcards(user: Annotated[UserIdentityResponse, Depends(get_active_user)], db: Annotated[Session, Depends(get_db)], request: Annotated[FlashcardDeleteBatchRequest, Query()]):
    user_id = user.user_id
    container = Container(db)
    factory = AppFactory(container)

    flashcard_service = factory.create(FlashcardServiceSQLAlchemy)
    flashcards_ids = flashcard_service.get_ids_by_public_ids_or_fail(user_id, request.public_ids)
    
    flashcard_service.delete_many(flashcards_ids)

    return FlashcardDeleteBatchResponse(
        deleted_public_ids=request.public_ids
    )