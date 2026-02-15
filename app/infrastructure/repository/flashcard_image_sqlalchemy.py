from sqlalchemy.orm import Session
from sqlalchemy import delete

from ...core.repositories.flashcard_images import FlashcardImagesRepository
from ...infrastructure.db.models import FlashcardImagesModel
from ...core.schemas.flashcards import FlashcardImage

class FlashcardImagesRepositorySQLAlchemy(FlashcardImagesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def delete_all_for_id(self, flashcard_id: int):
        stmt = delete(FlashcardImagesModel).where(FlashcardImagesModel.flashcard_id == flashcard_id)
        self.db_session.execute(stmt)
    
    def create_one(self, flashcard_id: int, image: FlashcardImage):
        image_model = FlashcardImagesModel(
            flashcard_id = flashcard_id,
            field = image.field,
            image_url= image.image_url
        )

        self.db_session.add(image_model)
    
    def create_many(self, flashcard_id: int, images: list[FlashcardImage]):
        image_models = []
        
        for image in images:
            image_model = FlashcardImagesModel(
                flashcard_id = flashcard_id,
                field = image.field,
                image_url= image.image_url
            )

            image_models.append(image_model)
        
        for image_model in image_models:
            self.db_session.add(image_model)