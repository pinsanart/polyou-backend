from sqlalchemy.orm import Session
from sqlalchemy import select

from ...core.repositories.flashcards_types import FlashcardTypesRepository
from ..db.models import FlashcardTypeModel

class FlashcardTypesRepositorySQLAlchemy(FlashcardTypesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id):
        stmt = select(FlashcardTypeModel).where(FlashcardTypeModel.flashcard_type_id == id)
        return self.db_session.scalar(stmt)

    def get_by_name(self, name: str):
        stmt = select(FlashcardTypeModel).where(FlashcardTypeModel.name == name)
        return self.db_session.scalar(stmt)