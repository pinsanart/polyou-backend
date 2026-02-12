from uuid import UUID
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from ...core.repositories.flashcards import FlashcardRepository
from ..db.models import FlashcardModel

class FlashcardRepositorySQLAlchemy(FlashcardRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, entity: FlashcardModel) -> FlashcardModel:
        self.db_session.add(entity)
        self.db_session.flush()
        return entity

    def list_ids(self, user_id: int):
        stmt = select(FlashcardModel.flashcard_id).where(FlashcardModel.user_id == user_id)
        return self.db_session.execute(stmt).scalars().all()

    def get_by_id(self, id: int) -> FlashcardModel | None:
        stmt = select(FlashcardModel).where(FlashcardModel.flashcard_id == id)
        return self.db_session.scalar(stmt)

    def get_by_public_id(self, public_id: UUID) -> FlashcardModel | None:
        stmt = select(FlashcardModel).where(FlashcardModel.public_id == public_id)
        return self.db_session.scalar(stmt)

    def list_by_ids(self, ids: List[int]) -> List[FlashcardModel]:
        if not ids:
            return []

        stmt = select(FlashcardModel).where(FlashcardModel.flashcard_id.in_(ids))
        return list(self.db_session.scalars(stmt).all())

    def update(self, id: int, data: dict) -> None:
        if not data:
            return
        
        stmt = update(FlashcardModel).where(FlashcardModel.flashcard_id == id).values(**data)
        self.db_session.execute(stmt)

    def delete(self, id: int) -> None:
        stmt = delete(FlashcardModel).where(FlashcardModel.flashcard_id == id)
        self.db_session.execute(stmt)