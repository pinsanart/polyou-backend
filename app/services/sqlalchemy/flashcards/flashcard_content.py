from ....core.services.flashcards.flashcard_content import FlashcardContentService
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_content import FlashcardContentRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardContentModel
from ....core.schemas.flashcards.models import FlashcardContent
from ....core.schemas.flashcards.bases import FlashcardContentBase

class FlashcardContentServiceSQLAlchemy(FlashcardContentService):
    def __init__(self, flashcard_content_repository: FlashcardContentRepositorySQLAlchemy):
        self.flashcard_content_repository = flashcard_content_repository
    
    def info(self, id: int) -> FlashcardContent:
        flashcard_content_model = self.flashcard_content_repository.get(id)

        if not flashcard_content_model:
            raise ValueError(f"Flashcard Content with id={id} not found.")
        
        return FlashcardContent.model_validate(flashcard_content_model)
    
    def change(self, id: int, new_content: FlashcardContentBase) -> None:
        flashcard_content_model = self.flashcard_content_repository.get(id)

        if not flashcard_content_model:
            raise ValueError(f"Flashcard Content with id={id} not found.")

        self.flashcard_content_repository.update(id, new_content.model_dump(exclude_unset=True))