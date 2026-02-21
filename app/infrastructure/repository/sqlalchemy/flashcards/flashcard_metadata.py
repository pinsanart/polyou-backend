from sqlalchemy.orm import Session

from .....core.repositories.flashcards.flashcard_metadata import FlashcardMetadataRepository

from .....infrastructure.db.models import FlashcardMetadataModel

class FlashcardMetadataRepositorySQLAlchemy(FlashcardMetadataRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, id: int) -> FlashcardMetadataModel:
        return self.db_session.get(FlashcardMetadataModel, id)
        
    def update(self, id, new_metadata: FlashcardMetadataModel) -> None:
        model = self.db_session.get(FlashcardMetadataModel, id)

        if not model:
            raise ValueError(f"Flashcard Metadata with id={id} not found.")

        model.created_at                = new_metadata.created_at
        model.last_audio_updated_at     = new_metadata.last_audio_updated_at
        model.last_content_updated_at   = new_metadata.last_content_updated_at
        model.last_image_updated_at     = new_metadata.last_image_updated_at
        model.last_review_at            = new_metadata.last_review_at