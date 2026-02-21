from sqlalchemy.orm import Session

from .....core.repositories.flashcards.flashcard_metadata import FlashcardMetadataRepository
from .....infrastructure.db.models import FlashcardMetadataModel

class FlashcardMetadataRepositorySQLAlchemy(FlashcardMetadataRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, id: int) -> FlashcardMetadataModel:
        return self.db_session.get(FlashcardMetadataModel, id)
        
    def update(self, id, data: dict) -> None:
        flashcard_metadata_model = self.db_session.get(FlashcardMetadataModel, id)

        if not flashcard_metadata_model:
            raise ValueError(f"Flashcard Metadata with id={id} not found.")

        for key, value in data.items():
            if hasattr(flashcard_metadata_model, key):
                setattr(flashcard_metadata_model, key, value)