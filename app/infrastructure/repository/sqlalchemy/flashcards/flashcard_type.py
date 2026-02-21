from sqlalchemy.orm import Session
from sqlalchemy import select

from .....core.repositories.flashcards.flashcard_type import FlashcardTypeRepository
from .....infrastructure.db.models import FlashcardTypeModel

class FlashcardTypeRepositorySQLAlchemy(FlashcardTypeRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_by_id(self, id: int) -> FlashcardTypeModel | None:
        return self.db_session.get(FlashcardTypeModel, id)
    
    def get_by_name(self, name) -> FlashcardTypeModel | None:
        stmt = select(FlashcardTypeModel).where(FlashcardTypeModel.name == name)
        return self.db_session.execute(stmt).scalar_one_or_none()

    def create(self, new_type: FlashcardTypeModel) -> None:
        self.db_session.add(new_type)
    
    def delete(self, id: int):
        db_model = self.db_session.get(FlashcardTypeModel, id)

        if not db_model:
            raise ValueError(f"Flashcard Type with id={id} not found")
    
        self.db_session.delete(db_model)