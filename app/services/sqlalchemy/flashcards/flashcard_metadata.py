from ....core.schemas.flashcards.bases import FlashcardMetadataBase
from ....core.schemas.flashcards.models import FlashcardMetadata
from ....core.services.flashcards.flashcard_metadata import FlashcardMetadataService
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_metadata import FlashcardMetadataRepositorySQLAlchemy

class FlashcardMetadataServiceSQLAlchemy(FlashcardMetadataService):
    def __init__(self, flashcard_metadata_repository: FlashcardMetadataRepositorySQLAlchemy):
        self.flashcard_metadata_repository = flashcard_metadata_repository

    def info_one(self, id: int) -> FlashcardMetadata:
        flashcard_metadata_model = self.flashcard_metadata_repository.get_one(id)

        if not flashcard_metadata_model:
            raise ValueError(f"Flashcard with id={id} not found.")
        
        return FlashcardMetadata.model_validate(flashcard_metadata_model)
    
    def info_all(self, user_id: int):
        flashcard_metadata_models = self.flashcard_metadata_repository.get_all(user_id)
        return [FlashcardMetadata.model_validate(model) for model in flashcard_metadata_models]

    def change(self, id, new_metadata: FlashcardMetadataBase) -> None:
        flashcard_metadata_model = self.flashcard_metadata_repository.get_one(id)

        if not flashcard_metadata_model:
            raise ValueError(f"Flashcard with id={id} not found.")
        
        self.flashcard_metadata_repository.update(id, new_metadata.model_dump(exclude_unset=True))