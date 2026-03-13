from pydantic import Field
from uuid import UUID, uuid4

from .bases import (
    FlashcardBase,
    FlashcardContentBase,
    FlashcardFSRSBase,
    FlashcardSyncMetadataBase,
    FlashcardReviewBase,
    FlashcardTypeBase,
    FlashcardMediaBase
)

class Flashcard(FlashcardBase):    
    flashcard_id: int
    user_id: int
    language_id: int
    flashcard_type_id: int

class FlashcardContent(FlashcardContentBase):
    flashcard_id: int

class FlashcardFSRS(FlashcardFSRSBase):
    flashcard_id: int

class FlashcardSyncMetadata(FlashcardSyncMetadataBase):
    flashcard_id: int

class FlashcardReview(FlashcardReviewBase):
    review_id: int
    flashcard_id: int

class FlashcardMedia(FlashcardMediaBase):
    media_id: int
    public_id: UUID = Field(default_factory=uuid4)

class FlashcardType(FlashcardTypeBase):
    flashcard_type_id: int