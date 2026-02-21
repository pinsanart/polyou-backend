from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.flashcards.flashcard_image import FlashcardImageRepository
from ....db.models import FlashcardImageModel

class FlashcardImageRepositorySQLAlchemy(FlashcardImageRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all(self, flashcard_id: int) -> List[FlashcardImageModel]:
        stmt = select(FlashcardImageModel).where(FlashcardImageModel.flashcard_id == flashcard_id)
        return self.db_session.scalars(stmt).all()

    def delete_all_for_id(self, flashcard_id: int) -> None:
        stmt = select(FlashcardImageModel).where(FlashcardImageModel.flashcard_id == flashcard_id)
        image_models = self.db_session.scalars(stmt).all()
        for image_model in image_models:
            self.db_session.delete(image_model)

    def create_one(self, image_model: FlashcardImageModel) -> None:
        self.db_session.add(image_model)
    
    def create_many(self, images_models: List[FlashcardImageModel]):
        self.db_session.add_all(images_models)