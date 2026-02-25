from typing import List

from ....core.services.flashcards.flashcard_image import FlashcardImageService
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_image import FlashcardImageRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardImageModel
from ....core.schemas.flashcards.models import FlashcardImage
from ....core.schemas.flashcards.bases import FlashcardImageBase

class FlashcadImageServiceSQLAlchemy(FlashcardImageService):
    def __init__(self, flashcard_image_repository: FlashcardImageRepositorySQLAlchemy):
        self.flashcard_image_repository = flashcard_image_repository
    
    def info_all(self, flashcard_id: int) -> List[FlashcardImage]:
        models = self.flashcard_image_repository.get_all(flashcard_id)
        return [FlashcardImage.model_validate(model) for model in models]
    
    def change(self, flashcard_id, new_images: List[FlashcardImageBase]) -> None:
        models = [
            FlashcardImageModel(
                flashcard_id = flashcard_id,
                **image.model_dump(exclude_unset=True)
            ) 
            for image in new_images
        ]
        self.flashcard_image_repository.delete_all_for_id(flashcard_id)
        self.flashcard_image_repository.create_many(models)