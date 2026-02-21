from ..core.schemas.flashcards.creates import FlashcardCreateInfo
from ..infrastructure.db.models import FlashcardModel

from ..infrastructure.db.models import (
    FlashcardModel,
    FlashcardMetadataModel,
    FlashcardContentModel,
    FlashcardFSRSModel,
    FlashcardReviewModel,
    FlashcardImageModel,
    FlashcardAudioModel
)

class FlashcardSQLAlchemyMapper:
    @staticmethod
    def to_model(user_id: int, create_info: FlashcardCreateInfo) -> FlashcardModel:
        flashcard_model = FlashcardModel(
            user_id=user_id,
            public_id=create_info.public_id,
            language_id=create_info.language_id,
            flashcard_type_id=create_info.flashcard_type_id
        )

        flashcard_model.server_metadata = FlashcardMetadataModel(
            **create_info.server_metadata.model_dump()
        )

        flashcard_model.content = FlashcardContentModel(
            **create_info.content.model_dump()
        )

        flashcard_model.fsrs = FlashcardFSRSModel(
            **create_info.fsrs.model_dump()
        )

        if create_info.reviews:
            flashcard_model.reviews = [
                FlashcardReviewModel(**review.model_dump())
                for review in create_info.reviews
            ]

        if create_info.images:
            flashcard_model.images = [
                FlashcardImageModel(**image.model_dump())
                for image in create_info.images
            ]

        if create_info.audios:
            flashcard_model.audios = [
                FlashcardAudioModel(**audio.model_dump())
                for audio in create_info.audios
            ]

        return flashcard_model