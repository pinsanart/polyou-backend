from .bases import (
    FlashcardBase,
    FlashcardContentBase,
    FlashcardFSRSBase,
    FlashcardImageBase,
    FlashcardTypeBase,
    FlashcardReviewBase
)

from ..languages.bases import ISOCode

class FlashcardCreateRequest(FlashcardBase):
    flashcard_type_name: str
    language_iso_639_1: ISOCode

class FlashcardContentRequest(FlashcardContentBase):
    pass

class FlashcardFSRSRequest(FlashcardFSRSBase):
    pass

class FlashcardImageRequest(FlashcardImageBase):
    pass

class FlashcardTypeRequest(FlashcardTypeBase):
    pass

class FlashcardReviewRequest(FlashcardReviewBase):
    pass