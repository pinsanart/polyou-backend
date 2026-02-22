from pydantic import BaseModel
from uuid import UUID
from typing import List

from .bases import (
    FlashcardBase,
    FlashcardMetadataBase
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

class FlashcardChangeContentResponse(FlashcardContentRequest):
    pass

class FlashcardChangeFSRSResponse(FlashcardFSRSRequest):
    pass

class FlashcardMetadataResponse(FlashcardMetadataBase):
    public_id: UUID

class FlashcardChangeImageResponse(FlashcardImageRequest):
    pass


class FlashcardChangeReviewResponse(FlashcardReviewRequest):
    pass

class FlashcardChangeAudioResponse(FlashcardAudioRequest):
    pass

class FlashcardChangeMetadataResponse(FlashcardMetadataRequest):
    pass

class FlaschardAllMetadataResponse(BaseModel):
    public_ids: List[UUID]
    metadatas: List[FlashcardMetadataResponse]