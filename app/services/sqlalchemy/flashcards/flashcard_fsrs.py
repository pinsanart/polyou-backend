from ....core.services.flashcards.flashcard_fsrs import FlashcardFSRSService
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_fsrs import FlashcardFSRSRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardFSRSModel
from ....core.schemas.flashcards.creates import FlashcardFSRSCreateInfo
from ....core.schemas.flashcards.models import FlashcardFSRS
from ....core.exceptions.flashcard_fsrs import FlashcardFSRSDoesNotExistError

class FlashcardFSRSServiceSQLAlchemy(FlashcardFSRSService):
    def __init__(self, flashcard_fsrs_repository: FlashcardFSRSRepositorySQLAlchemy):
        self.flashcard_fsrs_repository = flashcard_fsrs_repository
    
    def info(self, id: int) -> FlashcardFSRS:
        model = self.flashcard_fsrs_repository.get(id)

        if not model:
            raise FlashcardFSRSDoesNotExistError(f"Flashcard FSRS with id={id} not found.")

        return FlashcardFSRS.model_validate(model)

    def change(self, id: int, new_fsrs: FlashcardFSRSCreateInfo):
        model = self.flashcard_fsrs_repository.get(id)

        if not model:
            raise FlashcardFSRSDoesNotExistError(f"Flashcard FSRS with id={id} not found.")

        model = FlashcardFSRSModel(**new_fsrs.model_dump())
        self.flashcard_fsrs_repository.update(id, model)