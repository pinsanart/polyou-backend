from typing import List

from ..core.schemas.flashcards.models import (
    Flashcard,
    FlashcardSyncMetadata
)
from ..core.schemas.flashcards.responses import (
    FlashcardInfoResponse,
    FlashcardGetSyncMetadataResponse,
    FlashcardGetAllSyncMetadataResponse
)

from ..core.schemas.flashcards.bases import (
    FlashcardSyncMetadataBase
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
    
    def sync_metadata_to_response(self, user_id: int, sync_metadata: FlashcardSyncMetadata) -> FlashcardGetSyncMetadataResponse:
        data = sync_metadata.model_dump()

        flashcard_id = data.pop('flashcard_id')
        
        return FlashcardGetSyncMetadataResponse(
            public_id= self.flashcard_service.get_public_id_by_id_or_fail(user_id, flashcard_id),
            sync_metadata= FlashcardSyncMetadataBase(**data)
        )
        
    def all_sync_metadata_to_response(self, user_id: int, sync_metadatas: List[FlashcardSyncMetadata]) -> FlashcardGetAllSyncMetadataResponse:
        public_ids = []
        all_sync_metadata = []
        for sync_metadata in sync_metadatas:
            data = self.sync_metadata_to_response(user_id, sync_metadata)
            all_sync_metadata.append(data)
            public_ids.append(data.public_id)
        
        return FlashcardGetAllSyncMetadataResponse(
            public_ids=public_ids,
            sync_metadatas=all_sync_metadata
        )