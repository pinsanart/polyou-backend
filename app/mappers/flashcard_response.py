from ..core.schemas.flashcards.models import Flashcard
from ..core.schemas.flashcards.responses import FlashcardInfoResponse

from ..core.services.flashcards.flashcard_type import FlashcardTypeService
from ..core.services.languages.language import LanguageService

class FlashcardResponseMapper:
    def __init__(self, flashcard_type_service: FlashcardTypeService, language_service: LanguageService):
        self.flashcard_type_service = flashcard_type_service
        self.language_service = language_service

    def model_to_response(self, model: Flashcard) -> FlashcardInfoResponse:
        data = model.model_dump()

        data.pop('user_id')
        data.pop('flashcard_id')
        language_id = data.pop('language_id')
        flashcard_type_id = data.pop('flashcard_type_id')

        data['flashcard_type_name'] = self.flashcard_type_service.get_name_by_id_or_fail(flashcard_type_id)
        data['language_iso_639_1'] = self.language_service.get_iso_639_1_by_id_or_fail(language_id)

        return FlashcardInfoResponse(**data)