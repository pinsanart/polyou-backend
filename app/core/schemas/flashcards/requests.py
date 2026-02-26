from pydantic import BaseModel
from typing import List
from uuid import UUID

from .bases import (
    FlashcardBase,
    FlashcardContentBase,
    FlashcardFSRSBase,
    FlashcardImageBase,
    FlashcardTypeBase,
    FlashcardReviewBase,
    FlashcardAudioBase,
    FlashcardSyncMetadataBase
)

from ..languages.bases import ISOCode

class FlashcardPostRequest(FlashcardBase):
    flashcard_type_name: str
    language_iso_639_1: ISOCode

class FlashcardPostBatchRequest(BaseModel):
    flashcards: List[FlashcardPostRequest]

class FlashcardGetInfoRequest(BaseModel):
    public_ids: List[UUID]

class FlashcardGetSyncMetadataRequest(BaseModel):
    public_id: UUID

class FlashcardPatchContentRequest(BaseModel):
    public_id: UUID
    new_content: FlashcardContentBase

class FlashcardPatchFSRSRequest(BaseModel):
    public_id: UUID
    new_fsrs: FlashcardFSRSBase

class FlashcardPatchImagesRequest(BaseModel):
    public_id: UUID
    new_images: List[FlashcardImageBase]

class FlashcardPatchReviewsRequest(BaseModel):
    public_id: UUID
    new_reviews: List[FlashcardReviewBase]

class FlashcardPatchAudiosRequest(BaseModel):
    public_id: UUID
    new_audios: List[FlashcardAudioBase]
    
class FlashcardPatchSyncMetadataRequest(BaseModel):
    public_id: UUID
    new_sync_metadata: FlashcardSyncMetadataBase

class FlashcardDeleteRequest(BaseModel):
    public_id: UUID

class FlashcardDeleteBatchRequest(BaseModel):
    public_ids: List[UUID]

class FlashcardTypeRequest(FlashcardTypeBase):
    pass