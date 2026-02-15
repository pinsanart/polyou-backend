from sqlalchemy.orm import Session

from ...core.repositories.flashcard_content import FlashcardContentRepository
from ...core.schemas.flashcards import FlashcardContent
from ...infrastructure.db.models import FlashcardContentModel

class FlashcardContentRepositorySQLAlchemy(FlashcardContentRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def update(self, id: int, new_content: FlashcardContent):
        db_flashcard = (
            self.db_session.query(FlashcardContentModel)
            .filter(FlashcardContentModel.flashcard_id == id)
            .first()
        )

        db_flashcard.front_field_content = new_content.front_field
        db_flashcard.back_field_content = new_content.back_field