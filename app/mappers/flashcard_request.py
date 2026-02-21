from ..core.schemas.flashcards.creates import FlashcardCreateInfo
from ..core.schemas.flashcards.requests import FlashcardCreateRequest
from ..core.services.flashcards.flashcard_type import FlashcardTypeService
from ..core.services.languages.language import LanguageService

class FlashcardRequestMapper:
    def __init__(self, flashcard_type_service: FlashcardTypeService, language_service: LanguageService):
        self.flashcard_type_service = flashcard_type_service
        self.language_service = language_service

    def request_to_create(self, request: FlashcardCreateRequest) -> FlashcardCreateInfo:
        data = request.model_dump()

        flashcard_type_name = data.pop('flashcard_type_name')
        language_iso_639_1 = data.pop('language_iso_639_1')

        data['flashcard_type_id'] = self.flashcard_type_service.get_id_by_name_or_fail(flashcard_type_name) 
        data['language_id'] = self.language_service.get_id_by_iso_639_1_or_fail(language_iso_639_1)

        return FlashcardCreateInfo(**data)