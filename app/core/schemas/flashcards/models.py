from pydantic import ConfigDict

from .bases import (
    FlashcardBase,
    FlashcardContentBase,
    FlashcardAudioBase,
    FlashcardFSRSBase,
    FlashcardImageBase,
    FlashcardSyncMetadataBase,
    FlashcardReviewBase,
    FlashcardTypeBase
)

class Flashcard(FlashcardBase):    
    flashcard_id: int
    user_id: int
    language_id: int
    flashcard_type_id: int

class FlashcardContent(FlashcardContentBase):
    flashcard_id: int

class FlashcardAudio(FlashcardAudioBase):
    audio_id: int
    flashcard_id: int

class FlashcardFSRS(FlashcardFSRSBase):
    flashcard_id: int

class FlashcardImage(FlashcardImageBase):
    image_id: int
    flashcard_id: int

class FlashcardSyncMetadata(FlashcardSyncMetadataBase):
    flashcard_id: int

class FlashcardReview(FlashcardReviewBase):
    review_id: int
    flashcard_id: int

class FlashcardType(FlashcardTypeBase):
    flashcard_type_id: int