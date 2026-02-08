from ..core.services.flashcards_type import FlashcardTypesService
from ..infrastructure.repository.flashcards_type_sqlalchemy import FlashcardTypesRepositorySQLAlchemy
from ..core.exceptions.flashcard_types import FlashcardTypeDoNotExistError

class FlashcardsTypesServiceSQLAlchemy(FlashcardTypesService):
    def __init__(self, flashcards_types_repository:FlashcardTypesRepositorySQLAlchemy):
        super().__init__(flashcards_types_repository)
    
    def get_id_by_name_or_fail(self, name: int) ->int:
        flashcard_type = self.flashcards_types_repository.get_by_name(name)
        if not flashcard_type:
            raise FlashcardTypeDoNotExistError(f"The flashcard type {name} do not exist.")
        return flashcard_type.flashcard_type_id

    def get_name_by_id(self, id: int):
        model = self.flashcards_types_repository.get_by_id(id)
        return model.name