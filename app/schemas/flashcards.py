from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List


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

class FlashcardCreate(BaseModel):
    language_id: int
    flashcard_type_id: int

    images: list[FlashcardImage] | None = None
    audios: list[FlashcardAudio] | None = None
    content: FlashcardContent


class FlashcardIdentity(BaseModel):
    flashcard_id: int

class FlashcardReview(BaseModel):
    reviewd_at: datetime
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


class FlashcardInfo(BaseModel):
    flashcard_id: int

    language_id: int
    flashcard_type_id: int
    created_at: datetime
    updated_at: datetime

    content: FlashcardContent
    fsrs: FlashcardFSRS

    reviews: List[FlashcardReview] | None
    images: List[FlashcardImage] | None
    audios: List[FlashcardAudio] | None