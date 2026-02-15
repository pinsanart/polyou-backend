from ..core.services.flashcard_image import FlashcardImageService
from ..infrastructure.repository.flashcard_image_sqlalchemy import FlashcardImagesRepositorySQLAlchemy
from ..core.schemas.flashcards import FlashcardImage
from ..services.flashcards_sqlalchemy import FlashcardServiceSQLAlchemy

from uuid import UUID

class FlashcardImageServiceSQLAlchemy(FlashcardImageService):
    def __init__(self, flashcard_image_repository: FlashcardImagesRepositorySQLAlchemy, flashcard_service: FlashcardServiceSQLAlchemy):
        self.flashcard_image_repository = flashcard_image_repository
        self.flashcard_service = flashcard_service

    def update(self, user_id: int, public_id: UUID, new_images: list[FlashcardImage]):
        flashcard_id = self.flashcard_service.get_flashcard_id_by_public_id_or_fail(public_id, user_id)
        
        self.flashcard_image_repository.delete_all_for_id(flashcard_id)
        self.flashcard_image_repository.create_many(flashcard_id, new_images)