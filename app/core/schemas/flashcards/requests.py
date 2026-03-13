from pydantic import BaseModel, ConfigDict
from typing import List
from uuid import UUID
from datetime import datetime

from .bases import (
    FlashcardContentBase,
    FlashcardFSRSBase,
    FlashcardTypeBase,
    FlashcardReviewBase,
    FlashcardSyncMetadataBase
)

from ..languages.bases import ISOCode

class FlashcardPostRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    flashcard_type_name: str
    language_iso_639_1: ISOCode

    public_id: UUID
    created_at: datetime
    sync_metadata: FlashcardSyncMetadataBase
    content: FlashcardContentBase
    fsrs: FlashcardFSRSBase
    reviews: List[FlashcardReviewBase] | None = None

class FlashcardPostBatchRequest(BaseModel):
    flashcards: List[FlashcardPostRequest]

class FlashcardGetInfosRequest(BaseModel):
    public_ids: List[UUID]

class FlashcardGetSyncMetadataRequest(BaseModel):
    public_id: UUID

class FlashcardPatchContentRequest(BaseModel):
    public_id: UUID
    new_content: FlashcardContentBase

class FlashcardPatchFSRSRequest(BaseModel):
    public_id: UUID
    new_fsrs: FlashcardFSRSBase

class FlashcardPatchReviewsRequest(BaseModel):
    public_id: UUID
    new_reviews: List[FlashcardReviewBase]
    
class FlashcardPatchSyncMetadataRequest(BaseModel):
    public_id: UUID
    new_sync_metadata: FlashcardSyncMetadataBase

class FlashcardPutMediaRequest(BaseModel):
    flashcard_public_id: UUID

class FlashcardDeleteRequest(BaseModel):
    public_id: UUID

class FlashcardDeleteBatchRequest(BaseModel):
    public_ids: List[UUID]

class FlashcardTypeRequest(FlashcardTypeBase):
    pass