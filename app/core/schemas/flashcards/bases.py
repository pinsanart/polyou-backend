from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List

from uuid import UUID

from ....dependencies.time.utc_safe import utcnow

# =============================
# ENUMS
# =============================

from ...enums import (
    Fields,
    FSRSRating,
    FSRSState,
    MediaType
)

# =============================
# SCHEMAS
# =============================

class FlashcardTypeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None

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
    state: FSRSState = FSRSState.LEARNING

class FlashcardReviewBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    reviewed_at: datetime
    rating: FSRSRating
    response_time_ms: int
    
    scheduled_days: int
    actual_days: int

    prev_stability: float
    prev_difficulty: float
    new_stability: float
    new_difficulty: float

    state_before: FSRSState
    state_after: FSRSState

class FlashcardSyncMetadataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    last_review_at: datetime | None = None
    last_content_updated_at: datetime | None = None
    last_image_updated_at: datetime | None = None
    last_audio_updated_at: datetime | None = None

class FlashcardMediaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    field: Fields
    media_type: MediaType

    filename: str
    original_name: str
    file_type: str
    file_size: int
    created_at: datetime = Field(default_factory=utcnow)

class FlashcardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    public_id: UUID
    created_at: datetime

    sync_metadata: FlashcardSyncMetadataBase
    content: FlashcardContentBase
    fsrs: FlashcardFSRSBase
    reviews: List[FlashcardReviewBase] | None = None
    media: List[FlashcardMediaBase] | None = None