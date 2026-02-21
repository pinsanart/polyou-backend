from ....core.services.flashcards.flashcard_content import FlashcardContentService
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_content import FlashcardContentRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardContentModel
from ....core.schemas.flashcards.models import FlashcardContent
from ....core.schemas.flashcards.bases import FlashcardContentBase
from ....core.exceptions.flashcard_content import FlashcardContentDoesNotExistError

class FlashcardContentServiceSQLAlchemy(FlashcardContentService):
    def __init__(self, flashcard_content_repository: FlashcardContentRepositorySQLAlchemy):
        self.flashcard_content_repository = flashcard_content_repository
    
    def info(self, id: int) -> FlashcardContent:
        model = self.flashcard_content_repository.get(id)

        if not model:
            raise FlashcardContentDoesNotExistError(f"Flashcard Content with id={id} not found.")
        
        return FlashcardContent.model_validate(model)
    
    def change(self, id: int, new_content: FlashcardContentBase):
        model = self.flashcard_content_repository.get(id)

        if not model:
            raise FlashcardContentDoesNotExistError(f"Flashcard Content with id={id} not found.")
        
        model = FlashcardContentModel(**new_content.model_dump())

        self.flashcard_content_repository.update(id, model)