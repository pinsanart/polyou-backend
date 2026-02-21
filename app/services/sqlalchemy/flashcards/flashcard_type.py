from ....core.services.flashcards.flashcard_type import FlashcardTypeService
from ....core.exceptions.flashcard_types import FlashcardTypeDoNotExistError
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_type import FlashcardTypeRepositorySQLAlchemy
from ....core.schemas.flashcards.creates import FlashcardTypeCreateInfo
from ....infrastructure.db.models import FlashcardTypeModel

class FlashcardTypeServiceSQLAlchemy(FlashcardTypeService):
    def __init__(self, flashcard_type_repository: FlashcardTypeRepositorySQLAlchemy):
        self.flashcard_type_repository = flashcard_type_repository
    
    def get_id_by_name_or_fail(self, name: str) -> int:
        model = self.flashcard_type_repository.get_by_name(name)
        
        if not model:
            raise FlashcardTypeDoNotExistError(f"Flashcard Type with name='{name}' not found.")
        
        return model.flashcard_type_id
    
    def get_name_by_id_or_fail(self, id: int) -> str:
        model = self.flashcard_type_repository.get_by_id(id)
        
        if not model:
            raise FlashcardTypeDoNotExistError(f"Flashcard Type with id='{id}' not found.")
        
        return model.name
    
    def add(self, flashcard_type_info: FlashcardTypeCreateInfo):
        flashcard_type_model = FlashcardTypeModel(**flashcard_type_info.model_dump())
        self.flashcard_type_repository.create(flashcard_type_model)
        
    def delete(self, id: int):
        model = self.flashcard_type_repository.get_by_id(id)
        
        if not model:
            raise FlashcardTypeDoNotExistError(f"Flashcard Type with id='{id}' not found.")
        
        self.flashcard_type_repository.delete(id)