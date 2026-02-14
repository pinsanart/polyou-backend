from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List

from uuid import UUID

# =============================
# ENUMS
# =============================

class FieldsEnum(str, Enum):
    front = "front"
    back = "back"

class StateEnum(int, Enum):
    LEARNING = 1
    REVIEW = 2
    RELEARNING = 3

class RatingEnum(int, Enum):
    AGAIN = 1
    HARD = 2
    GOOD = 3

# =============================
# SCHEMAS
# =============================

class FlashcardTypes(BaseModel):
    flashcard_type_id: int
    type: str
    description: str | None = None

class FlashcardImage(BaseModel):
    field: FieldsEnum
    image_url: str

class FlashcardAudio(BaseModel):
    field: FieldsEnum
    audio_url: str

class FlashcardContent(BaseModel):
    front_field: str
    back_field: str | None = None

class FlashcardFSRS(BaseModel):
    stability: float = 0.1
    difficulty: float = 5.0
    due: datetime = Field(default_factory=datetime.today)
    last_review: datetime | None = None
    state: StateEnum = StateEnum.LEARNING

class FlashcardIdentity(BaseModel):
    public_id: UUID

class FlashcardReview(BaseModel):
    reviewed_at: datetime
    rating: RatingEnum
    response_time_ms: int
    
    scheduled_days: int
    actual_days: int

    prev_stability: float
    prev_difficulty: float
    new_stability: float
    new_difficulty: float

    state_before: StateEnum
    state_after: StateEnum

class FlashcardServerInformation(BaseModel):
    created_at: datetime
    last_review_at: datetime | None = None
    last_content_updated_at: datetime | None = None

class FlashcardInfo(BaseModel):
    public_id: UUID

    language_iso_639_1: str
    flashcard_type_name: str
    
    server_information: FlashcardServerInformation
    
    content: FlashcardContent
    fsrs: FlashcardFSRS
    reviews: List[FlashcardReview] | None
    images: List[FlashcardImage] | None
    audios: List[FlashcardAudio] | None

class FlashcardCreateInfo(BaseModel):
    public_id: UUID

    language_iso_639_1: str
    flashcard_type_name: str
    
    server_information: FlashcardServerInformation | None = None

    content: FlashcardContent
    fsrs: FlashcardFSRS
    reviews: List[FlashcardReview] | None = None
    images: List[FlashcardImage] | None = None
    audios: List[FlashcardAudio] | None = None

class FlashcardCreateResponse(BaseModel):
    public_id: UUID

class FlashcardsCreateBatchReponseModel(BaseModel):
    public_ids: list[UUID]