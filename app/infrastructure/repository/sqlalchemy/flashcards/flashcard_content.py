from sqlalchemy.orm import Session

from .....core.repositories.flashcards.flashcard_content import FlashcardContentRepository
from ....db.models import FlashcardContentModel

class FlashcardContentRepositorySQLAlchemy(FlashcardContentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, id) -> FlashcardContentModel:
        return self.db_session.get(FlashcardContentModel, id)
    
    def update(self, id: int, new_content: FlashcardContentModel):
        model = self.db_session.get(FlashcardContentModel, id)

        if not model:
            raise ValueError(f"Flashcard Content with id={id} not found.")
        
        model.front_field_content = new_content.front_field_content
        model.back_field_content = new_content.back_field_content