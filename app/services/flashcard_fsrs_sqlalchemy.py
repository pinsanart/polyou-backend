from uuid import UUID

from ..core.services.flashcards.flashcard_fsrs import FlashcardFSRSService
from ..infrastructure.repository.flashcard_fsrs_sqlalchemy import FlashcardFSRSRepositorySQLAlchemy
from ..services.flashcards_sqlalchemy import FlashcardServiceSQLAlchemy
from ..core.schemas.flashcards import FlashcardFSRS

class FlashcardFSRSServiceSQLAlchemy(FlashcardFSRSService):
    def __init__(self, flashcard_fsrs_repository: FlashcardFSRSRepositorySQLAlchemy, flashcard_service: FlashcardServiceSQLAlchemy):
        self.flashcard_fsrs_repository = flashcard_fsrs_repository
        self.flashcard_service = flashcard_service
    
    def change(self, user_id: int, public_id: UUID, new_fsrs: FlashcardFSRS):
        flashcard_id = self.flashcard_service.get_flashcard_id_by_public_id_or_fail(public_id, user_id)
        self.flashcard_fsrs_repository.update(flashcard_id, new_fsrs)