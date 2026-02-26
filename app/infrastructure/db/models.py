from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime,
    Date,
    Boolean,
    Enum as SQLEnum,
)
from uuid import UUID, uuid4

from typing import List, Optional
from datetime import datetime

from ...dependencies.time.utc_safe import utcnow

# =========================================================
# Enums
# =========================================================

from ...core.enums import (
    Fields,
    FSRSRating,
    FSRSState
)

# =========================================================
# Base
# =========================================================
class PolyouDB(DeclarativeBase):
    pass

# =========================================================
# Users
# =========================================================
class UserCredentialsModel(PolyouDB):
    __tablename__ = "users_credentials"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="credentials")

class UserMetadataModel(PolyouDB):
    __tablename__ = "users_metadata"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="user_metadata")

class UserModel(PolyouDB):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    
    user_metadata: Mapped["UserMetadataModel"] = relationship(
        back_populates='user',
        uselist=False,
        cascade="all, delete-orphan"
    )

    profile: Mapped["UserProfileModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    credentials: Mapped["UserCredentialsModel"] = relationship(
        back_populates='user',
        uselist=False,
        cascade="all, delete-orphan"
    )

    known_languages: Mapped[List["UserKnownLanguageModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    target_languages: Mapped[List["UserTargetLanguageModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    flashcards: Mapped[List["FlashcardModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    refresh_tokens: Mapped[List["RefreshTokenModel"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

class UserProfileModel(PolyouDB):
    __tablename__ = "users_profile"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    birth: Mapped[Optional[datetime.date]] = mapped_column(Date)

    user: Mapped["UserModel"] = relationship(back_populates="profile")

class RefreshTokenModel(PolyouDB):
    __tablename__ = "users_refresh_tokens"

    refresh_token_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id', ondelete="CASCADE"),
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(64), 
        nullable=False, 
        unique=True,
        index=True    
    )

    device_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), 
        nullable=False,
        index=True
    )

    device_name: Mapped[str] = mapped_column(String, nullable=False)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
    user_agent: Mapped[str] = mapped_column(String, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    replaced_by: Mapped[Optional[int]] = mapped_column(
       ForeignKey("users_refresh_tokens.refresh_token_id"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(default=utcnow, nullable=False)
    
    user: Mapped["UserModel"] = relationship(back_populates="refresh_tokens")

# =========================================================
# Languages
# =========================================================
class LanguageModel(PolyouDB):
    __tablename__ = "languages"

    language_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    iso_639_1: Mapped[str] = mapped_column(String(2), nullable=False, unique=True)

    known_by_users: Mapped[List["UserKnownLanguageModel"]] = relationship(back_populates="language")
    target_by_users: Mapped[List["UserTargetLanguageModel"]] = relationship(back_populates="language")
    flashcards: Mapped[List["FlashcardModel"]] = relationship(back_populates="language")


class UserKnownLanguageModel(PolyouDB):
    __tablename__ = "user_known_languages"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    language_id: Mapped[int] = mapped_column(
        ForeignKey("languages.language_id", ondelete="CASCADE"),
        primary_key=True
    )

    user: Mapped["UserModel"] = relationship(back_populates="known_languages")
    language: Mapped["LanguageModel"] = relationship(back_populates="known_by_users")


# =========================================================
# Target Languages
# =========================================================

class UserTargetLanguageModel(PolyouDB):
    __tablename__ = "user_target_languages"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    language_id: Mapped[int] = mapped_column(
        ForeignKey("languages.language_id", ondelete="CASCADE"),
        primary_key=True
    )
    
    user: Mapped["UserModel"] = relationship(back_populates="target_languages")
    language: Mapped["LanguageModel"] = relationship(back_populates="target_by_users")


# =========================================================
# Flashcards
# =========================================================
class FlashcardTypeModel(PolyouDB):
    __tablename__ = "flashcard_types"

    flashcard_type_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String)

    flashcards: Mapped[List["FlashcardModel"]] = relationship(back_populates="flashcard_type")


class FlashcardSyncMetadataModel(PolyouDB):
    __tablename__ = "flashcards_sync_metadata"

    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.flashcard_id", ondelete="CASCADE"),
        primary_key=True
    )

    last_review_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_content_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_image_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    last_audio_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    flashcard: Mapped["FlashcardModel"] = relationship(
        back_populates="sync_metadata",
        passive_deletes=True
    )

class FlashcardModel(PolyouDB):
    __tablename__ = "flashcards"

    flashcard_id: Mapped[int] = mapped_column(primary_key=True)
    
    public_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
        index=True      
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.language_id"), nullable=False)
    flashcard_type_id: Mapped[int] = mapped_column(ForeignKey("flashcard_types.flashcard_type_id"), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="flashcards")
    language: Mapped["LanguageModel"] = relationship(back_populates="flashcards")
    flashcard_type: Mapped["FlashcardTypeModel"] = relationship(back_populates="flashcards")

    sync_metadata: Mapped["FlashcardSyncMetadataModel"] = relationship(
        back_populates="flashcard",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    content: Mapped["FlashcardContentModel"] = relationship(
        back_populates="flashcard",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    fsrs: Mapped["FlashcardFSRSModel"] = relationship(
        back_populates="flashcard",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    
    reviews: Mapped[List["FlashcardReviewModel"]] = relationship(
        back_populates="flashcard",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    images: Mapped[List["FlashcardImageModel"]] = relationship(
        back_populates="flashcard",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    audios: Mapped[List["FlashcardAudioModel"]] = relationship(
        back_populates="flashcard",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

class FlashcardContentModel(PolyouDB):
    __tablename__ = "flashcards_content"

    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.flashcard_id", ondelete="CASCADE"),
        primary_key=True
    )

    front_field: Mapped[str] = mapped_column(String, nullable=False)
    back_field: Mapped[Optional[str]] = mapped_column(String)

    flashcard: Mapped["FlashcardModel"] = relationship(
        back_populates="content",
        passive_deletes=True
    )

class FlashcardFSRSModel(PolyouDB):
    __tablename__ = "flashcards_fsrs"

    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.flashcard_id", ondelete="CASCADE"),
        primary_key=True
    )
    stability: Mapped[float] = mapped_column(nullable=False, default=0.3)
    difficulty: Mapped[float] = mapped_column(nullable=False, default=5.0)
    due: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    last_review: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    state: Mapped[FSRSState] = mapped_column(SQLEnum(FSRSState), nullable=False, default=FSRSState.LEARNING)

    flashcard: Mapped["FlashcardModel"] = relationship(
        back_populates="fsrs",
        passive_deletes=True
    )

class FlashcardReviewModel(PolyouDB):
    __tablename__ = "flashcards_reviews"

    review_id: Mapped[int] = mapped_column(primary_key=True)
    
    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.flashcard_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    reviewed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=utcnow, 
        nullable=False
    )
    
    rating: Mapped[FSRSRating] = mapped_column(SQLEnum(FSRSRating), nullable=False)
    
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    
    scheduled_days: Mapped[int] = mapped_column(Integer, nullable=False)
    actual_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    prev_stability: Mapped[float] = mapped_column(nullable=False)
    prev_difficulty: Mapped[float] = mapped_column(nullable=False)
    new_stability: Mapped[float] = mapped_column(nullable=False)
    new_difficulty: Mapped[float] = mapped_column(nullable=False)
    
    state_before: Mapped[FSRSState] = mapped_column(SQLEnum(FSRSState), nullable=False)
    state_after: Mapped[FSRSState] = mapped_column(SQLEnum(FSRSState), nullable=False)

    flashcard: Mapped["FlashcardModel"] = relationship(
        back_populates="reviews",
        passive_deletes = True
    )


class FlashcardImageModel(PolyouDB):
    __tablename__ = "flashcards_images"

    image_id: Mapped[int] = mapped_column(primary_key=True)
    
    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.flashcard_id", ondelete="CASCADE"),
        nullable=False
    )

    field: Mapped[Fields] = mapped_column(SQLEnum(Fields), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    flashcard: Mapped["FlashcardModel"] = relationship(
        back_populates="images",
        passive_deletes=True
    )

class FlashcardAudioModel(PolyouDB):
    __tablename__ = "flashcards_audios"

    audio_id: Mapped[int] = mapped_column(primary_key=True)
    
    flashcard_id: Mapped[int] = mapped_column(
        ForeignKey("flashcards.flashcard_id", ondelete="CASCADE"),
        nullable=False
    )
    
    field: Mapped[Fields] = mapped_column(SQLEnum(Fields), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)

    flashcard: Mapped["FlashcardModel"] = relationship(
        back_populates="audios",
        passive_deletes=True
    )

# =========================================================
# Create / Drop (opcional)
# =========================================================
#from connection import engine
#PolyouDB.metadata.drop_all(engine)
#PolyouDB.metadata.create_all(engine)