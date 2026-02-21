from .bases import (
    FlashcardBase
)

from ..languages.bases import ISOCode

class FlashcardCreateRequest(FlashcardBase):
    flashcard_type_name: str
    language_iso_639_1: ISOCode