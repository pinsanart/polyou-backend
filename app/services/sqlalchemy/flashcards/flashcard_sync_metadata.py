from ....core.schemas.flashcards.bases import FlashcardSyncMetadataBase
from ....core.schemas.flashcards.models import FlashcardSyncMetadata
from ....core.services.flashcards.flashcard_sync_metadata import FlashcardSyncMetadataService
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_sync_metadata import FlashcardSyncMetadataRepositorySQLAlchemy

class FlashcardSyncMetadataServiceSQLAlchemy(FlashcardSyncMetadataService):
    def __init__(self, flashcard_metadata_repository: FlashcardSyncMetadataRepositorySQLAlchemy):
        self.flashcard_metadata_repository = flashcard_metadata_repository

    def info_one(self, id: int) -> FlashcardSyncMetadata:
        flashcard_metadata_model = self.flashcard_metadata_repository.get_one(id)

        if not flashcard_metadata_model:
            raise ValueError(f"Flashcard with id={id} not found.")
        
        return FlashcardSyncMetadata.model_validate(flashcard_metadata_model)
    
    def info_all(self, user_id: int):
        flashcard_metadata_models = self.flashcard_metadata_repository.get_all(user_id)
        return [FlashcardSyncMetadata.model_validate(model) for model in flashcard_metadata_models]

    def change(self, id, new_metadata: FlashcardSyncMetadataBase) -> None:
        flashcard_metadata_model = self.flashcard_metadata_repository.get_one(id)

        if not flashcard_metadata_model:
            raise ValueError(f"Flashcard with id={id} not found.")
        
        self.flashcard_metadata_repository.update(id, new_metadata.model_dump(exclude_unset=True))