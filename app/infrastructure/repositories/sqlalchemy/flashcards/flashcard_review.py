from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.flashcards.flashcard_review import FlashcardReviewRepository
from .....infrastructure.db.models import FlashcardReviewModel

class FlashcardReviewRepositorySQLAlchemy(FlashcardReviewRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_all(self, flashcard_id: int) -> List[FlashcardReviewModel]:
        stmt = select(FlashcardReviewModel).where(FlashcardReviewModel.flashcard_id == flashcard_id)
        return self.db_session.scalars(stmt).all()
    
    def create_one(self, review_model: FlashcardReviewModel):
        self.db_session.add(review_model)

    def create_many(self, review_models: List[FlashcardReviewModel]):
        self.db_session.add_all(review_models)
    
    def delete_all_for_id(self, flashcard_id: int):
        stmt = select(FlashcardReviewModel).where(FlashcardReviewModel.flashcard_id == flashcard_id)
        flashcard_review_models = self.db_session.scalars(stmt).all()
        for image_model in flashcard_review_models:
            self.db_session.delete(image_model)