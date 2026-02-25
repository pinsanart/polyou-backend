from typing import List

from ....core.schemas.flashcards.models import FlashcardReview
from ....core.schemas.flashcards.bases import FlashcardReviewBase
from ....core.services.flashcards.flashcard_review import FlashcardReviewService
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_review import FlashcardReviewRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardReviewModel

class FlashcardReviewServiceSQLAlchemy(FlashcardReviewService):
    def __init__(self, flashcard_review_repository: FlashcardReviewRepositorySQLAlchemy):
        self.flashcard_review_repository = flashcard_review_repository
    
    def info_all(self, flashcard_id: int) -> List[FlashcardReview]:
        flashcard_reviews_models = self.flashcard_review_repository.get_all(flashcard_id)
        return [FlashcardReview.model_validate(review_model) for review_model in flashcard_reviews_models]
    
    def change(self, flashcard_id: int, new_reviews: List[FlashcardReviewBase]):
        models = [
            FlashcardReviewModel(
                flashcard_id = flashcard_id,
                **new_review.model_dump()
            )
            for new_review in new_reviews
        ]

        self.flashcard_review_repository.delete_all_for_id(flashcard_id)
        self.flashcard_review_repository.create_many(models)