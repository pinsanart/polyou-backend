from pydantic import BaseModel, Field, ConfigDict
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

class FlashcardTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None

class FlashcardImageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    field: FieldsEnum
    url: str

class FlashcardAudioBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    field: FieldsEnum
    url: str

class FlashcardContentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    front_field: str
    back_field: str | None = None

class FlashcardFSRSBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stability: float = 0.1
    difficulty: float = 5.0
    due: datetime = Field(default_factory=datetime.today)
    last_review: datetime | None = None
    state: StateEnum = StateEnum.LEARNING

class FlashcardReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

class FlashcardSyncMetadataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    last_review_at: datetime | None = None
    last_content_updated_at: datetime | None = None
    last_image_updated_at: datetime | None = None
    last_audio_updated_at: datetime | None = None

class FlashcardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: UUID
    created_at: datetime

    sync_metadata: FlashcardSyncMetadataBase
    content: FlashcardContentBase
    fsrs: FlashcardFSRSBase
    reviews: List[FlashcardReviewBase] | None = None
    images: List[FlashcardImageBase] | None = None
    audios: List[FlashcardAudioBase] | None = None