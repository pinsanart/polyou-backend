from typing import List

from ..core.schemas.flashcards.models import (
    Flashcard,
    FlashcardSyncMetadata
)
from ..core.schemas.flashcards.responses import (
    FlashcardInfoResponse,
    FlashcardMetadataResponse,
    FlaschardAllMetadataResponse
)

from ..core.services.flashcards.flashcard_type import FlashcardTypeService
from ..core.services.languages.language import LanguageService
from ..core.services.flashcards.flashcard import FlashcardService

class FlashcardResponseMapper:
    def __init__(self, flashcard_service: FlashcardService, flashcard_type_service: FlashcardTypeService, language_service: LanguageService):
        self.flashcard_service = flashcard_service
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
    
    def metadata_to_response(self, user_id: int, metadata: FlashcardSyncMetadata) -> FlashcardMetadataResponse:
        data = metadata.model_dump()

        flashcard_id = data.pop('flashcard_id')
        
        data['public_id'] = self.flashcard_service.get_public_id_by_id_or_fail(user_id, flashcard_id)

        return FlashcardMetadataResponse(**data)
    
    def all_metadata_to_response(self, user_id: int, metadatas: List[FlashcardSyncMetadata]) -> FlaschardAllMetadataResponse:
        public_ids = []
        all_metadata = []
        for metadata in metadatas:
            data = self.metadata_to_response(user_id, metadata)
            all_metadata.append(data)
            public_ids.append(data.public_id)
        
        return FlaschardAllMetadataResponse(
            public_ids= public_ids,
            metadatas= all_metadata
        )
