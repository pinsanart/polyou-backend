from pydantic import BaseModel
from uuid import UUID
from typing import List

from .bases import (
    FlashcardBase,
    FlashcardSyncMetadataBase
)

from .requests import (
    FlashcardContentRequest,
    FlashcardFSRSRequest,
    FlashcardImageRequest,
    FlashcardReviewRequest,
    FlashcardAudioRequest,
    FlashcardMetadataRequest
)

from ..languages.bases import ISOCode

class FlashcardCreateResponse(BaseModel):
    public_id: UUID

class FlashcardCreateBatchResponse(BaseModel):
    public_ids: List[UUID]

class UserFlashcardsPublicIdsResponse(BaseModel):
    public_ids: List[UUID]

class FlashcardDeleteResponse(BaseModel):
    deleted_public_id: UUID

class FlashcardDeleteBatchResponse(BaseModel):
    deleted_public_ids: List[UUID]

class FlashcardInfoResponse(FlashcardBase):
    language_iso_639_1: ISOCode
    flashcard_type_name: str

class FlashcardChangeContentResponse(BaseModel):
    public_id: UUID
    new_content: FlashcardContentRequest

class FlashcardChangeFSRSResponse(BaseModel):
    public_id: UUID
    new_fsrs: FlashcardFSRSRequest

class FlashcardMetadataResponse(FlashcardSyncMetadataBase):
    public_id: UUID

class FlashcardChangeImagesResponse(BaseModel):
    public_id: UUID
    new_images: List[FlashcardImageRequest]

class FlashcardChangeReviewsResponse(BaseModel):
    public_id: UUID
    new_reviews: List[FlashcardReviewRequest]

class FlashcardChangeAudiosResponse(BaseModel):
    public_id: UUID
    new_audios: List[FlashcardAudioRequest]

class FlashcardChangeMetadataResponse(BaseModel):
    public_id: UUID
    new_metadata: FlashcardMetadataRequest

class FlaschardAllMetadataResponse(BaseModel):
    public_ids: List[UUID]
    metadatas: List[FlashcardMetadataResponse]