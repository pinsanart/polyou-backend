from .bases import (
    FlashcardBase,
    FlashcardTypeBase,
    FlashcardFSRSBase,
    FlashcardImageBase
)

class FlashcardCreateInfo(FlashcardBase):
    language_id: int
    flashcard_type_id: int

class FlashcardTypeCreateInfo(FlashcardTypeBase):
    pass

class FlashcardFSRSCreateInfo(FlashcardFSRSBase):
    pass

class FlascahrdImageCreateInfo(FlashcardImageBase):
    pass