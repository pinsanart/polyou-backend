from pydantic import BaseModel
from uuid import UUID
from typing import List

from .bases import (
    FlashcardBase
)

from .requests import (
    FlashcardContentRequest
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