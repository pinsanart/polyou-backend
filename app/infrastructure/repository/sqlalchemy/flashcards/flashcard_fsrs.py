from sqlalchemy.orm import Session

from .....core.repositories.flashcards.flashcard_fsrs import FlashcardFSRSRepository
from ....db.models import FlashcardFSRSModel

class FlashcardFSRSRepositorySQLAlchemy(FlashcardFSRSRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, id: int):
        return self.db_session.get(FlashcardFSRSModel, id)
    
    def update(self, id: int, new_fsrs: FlashcardFSRSModel):
        model = self.db_session.get(FlashcardFSRSModel, id)

        if not model:
            raise ValueError(f"Flashcard FSRS with id={id} not found.")

        model.difficulty    = new_fsrs.difficulty
        model.due           = new_fsrs.due
        model.last_review   = new_fsrs.last_review
        model.stability     = new_fsrs.stability
        model.state         = new_fsrs.state