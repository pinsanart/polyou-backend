from uuid import UUID

from ..core.services.flashcard_content import FlashcardContentService
from ..infrastructure.repository.flashcard_content_sqlalchemy import FlashcardContentRepositorySQLAlchemy
from ..services.flashcards_sqlalchemy import FlashcardServiceSQLAlchemy

from ..core.schemas.flashcards import FlashcardContent

class FlashcardContentServiceSQLAlchemy(FlashcardContentService):
    def __init__(self, flashcard_content_repository: FlashcardContentRepositorySQLAlchemy, flashcard_service: FlashcardServiceSQLAlchemy):
        self.flashcard_content_repository = flashcard_content_repository
        self.flashcard_service = flashcard_service
    
    def change(self, user_id: int, public_id: UUID, new_content: FlashcardContent):
        flashcard_id = self.flashcard_service.get_flashcard_id_by_public_id_or_fail(public_id, user_id)
        self.flashcard_content_repository.update(flashcard_id, new_content)