from ....core.services.flashcards.flashcard_fsrs import FlashcardFSRSService
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_fsrs import FlashcardFSRSRepositorySQLAlchemy
from ....core.schemas.flashcards.bases import FlashcardFSRSBase
from ....core.schemas.flashcards.models import FlashcardFSRS

class FlashcardFSRSServiceSQLAlchemy(FlashcardFSRSService):
    def __init__(self, flashcard_fsrs_repository: FlashcardFSRSRepositorySQLAlchemy):
        self.flashcard_fsrs_repository = flashcard_fsrs_repository
    
    def info(self, id: int) -> FlashcardFSRS:
        flashcard_fsrs_model = self.flashcard_fsrs_repository.get(id)

        if not flashcard_fsrs_model:
            raise ValueError(f"Flashcard FSRS with id={id} not found.")

        return FlashcardFSRS.model_validate(flashcard_fsrs_model)

    def change(self, id: int, new_fsrs: FlashcardFSRSBase) -> None:
        flashcard_fsrs_model = self.flashcard_fsrs_repository.get(id)

        if not flashcard_fsrs_model:
            raise ValueError(f"Flashcard FSRS with id={id} not found.")
        
        self.flashcard_fsrs_repository.update(id, new_fsrs.model_dump(exclude_unset=True))