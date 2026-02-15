from sqlalchemy.orm import Session

from ...core.repositories.flashcard_fsrs import FlashcardFSRSRepository
from ...core.schemas.flashcards import FlashcardFSRS
from ..db.models import FlashcardFSRSModel

class FlashcardFSRSRepositorySQLAlchemy(FlashcardFSRSRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def update(self, id: int, new_fsrs: FlashcardFSRS):
        db_flashcard = (
            self.db_session.query(FlashcardFSRSModel)
            .filter(FlashcardFSRSModel.flashcard_id == id)
            .first()
        )

        db_flashcard.stability = new_fsrs.stability
        db_flashcard.difficulty = new_fsrs.difficulty
        db_flashcard.due = new_fsrs.due
        db_flashcard.last_review = new_fsrs.last_review
        db_flashcard.state = new_fsrs.state