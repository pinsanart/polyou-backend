from sqlalchemy.orm import Session

from .....core.repositories.flashcards.flashcard_content import FlashcardContentRepository
from ....db.models import FlashcardContentModel

class FlashcardContentRepositorySQLAlchemy(FlashcardContentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, id) -> FlashcardContentModel:
        return self.db_session.get(FlashcardContentModel, id)
    
    def update(self, id: int, data: dict):
        flashcard_content_model = self.db_session.get(FlashcardContentModel, id)

        if not flashcard_content_model:
            raise ValueError(f"Flashcard Content with id={id} not found.")
        
        for key, value in data.items():
            if hasattr(flashcard_content_model, key):
                setattr(flashcard_content_model, key, value)     