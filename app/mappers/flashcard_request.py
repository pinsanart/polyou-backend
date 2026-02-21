from ..core.schemas.flashcards.requests import FlashcardCreateRequest
from ..core.services.flashcards.flashcard_type import FlashcardTypeService
from ..core.services.languages.language import LanguageService

from ..infrastructure.db.models import (
    FlashcardModel,
    FlashcardMetadataModel,
    FlashcardContentModel,
    FlashcardFSRSModel,
    FlashcardReviewModel,
    FlashcardImageModel,
    FlashcardAudioModel
)

class FlashcardRequestMapper:
    def __init__(self, flashcard_type_service: FlashcardTypeService, language_service: LanguageService):
        self.flashcard_type_service = flashcard_type_service
        self.language_service = language_service
    
    def request_to_db_model(self, user_id: int, create_info: FlashcardCreateRequest) -> FlashcardModel:
        flashcard_model = FlashcardModel(
            user_id=user_id,
            public_id=create_info.public_id,
            language_id= self.language_service.get_id_by_iso_639_1_or_fail(create_info.language_iso_639_1),
            flashcard_type_id= self.flashcard_type_service.get_id_by_name_or_fail(create_info.flashcard_type_name)
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