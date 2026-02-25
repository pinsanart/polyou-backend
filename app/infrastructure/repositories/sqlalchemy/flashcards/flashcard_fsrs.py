from sqlalchemy.orm import Session

from .....core.repositories.flashcards.flashcard_fsrs import FlashcardFSRSRepository
from ....db.models import FlashcardFSRSModel

class FlashcardFSRSRepositorySQLAlchemy(FlashcardFSRSRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, id: int):
        return self.db_session.get(FlashcardFSRSModel, id)
    
    def update(self, id: int, data: dict):
        flashcard_fsrs_model = self.db_session.get(FlashcardFSRSModel, id)

        if not flashcard_fsrs_model:
            raise ValueError(f"Flashcard FSRS with id={id} not found.")

        for key, value in data.items():
            if hasattr(flashcard_fsrs_model, key):
                setattr(flashcard_fsrs_model, key, value)     