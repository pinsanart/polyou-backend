from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import List
from uuid import UUID

from .....core.repositories.flashcards.flashcard_media import FlashcardMediaRepository
from .....infrastructure.db.models import FlashcardMediaModel

class FlashcardMediaRepositorySQLAlchemy(FlashcardMediaRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_by_id(self, id: int) -> FlashcardMediaModel | None:
        return self.db_session.get(FlashcardMediaModel, id)
    
    def get_by_flashcard_id(self, flashcard_id: int) -> List[FlashcardMediaModel]:
        stmt = select(FlashcardMediaModel).where(FlashcardMediaModel.flashcard_id == flashcard_id)
        return self.db_session.scalars(stmt).all()
    
    def get_by_public_id(self, public_id: UUID) -> FlashcardMediaModel | None:
        stmt = select(FlashcardMediaModel).where(FlashcardMediaModel.public_id == public_id)
        return self.db_session.scalar(stmt)

    def get_by_ids(self, ids: List[int]) -> List[FlashcardMediaModel]:
        stmt = select(FlashcardMediaModel).where(FlashcardMediaModel.media_id.in_(ids))
        return self.db_session.scalars(stmt).all()

    def get_by_public_ids(self, public_ids: List[UUID]) -> List[FlashcardMediaModel]:
        stmt = select(FlashcardMediaModel).where(FlashcardMediaModel.public_id.in_(public_ids))
        return self.db_session.scalars(stmt).all()

    def create_one(self, model: FlashcardMediaModel):
        self.db_session.add(model)

    def create_many(self, models: List[FlashcardMediaModel]) -> None:
        self.db_session.add_all(models)

    def delete_many_by_ids(self, ids: List[int]) -> None:
        models = self.get_by_ids(ids)

        if len(models) != len(ids):
            raise ValueError("Some FlashcardMedia not found.")

        for model in models:
            self.db_session.delete(model)

    def delete_one_by_id(self, id: int) -> None:
        model = self.db_session.get(FlashcardMediaModel, id)

        if not model:
            raise ValueError(f"Flashcard Media with id={id} not found.")
        
        self.db_session.delete(model)

    def delete_many_by_public_ids(self, public_ids: List[UUID]) -> None:
        models = self.get_by_public_ids(public_ids)

        if len(models) != len(public_ids):
            raise ValueError("Some FlashcardMedia not found.")

        for model in models:
            self.db_session.delete(model)
    
    def delete_one_by_public_id(self, public_id: UUID):
        stmt = select(FlashcardMediaModel).where(FlashcardMediaModel.public_id == public_id)
        model = self.db_session.scalar(stmt)
        
        if not model:
            raise ValueError(f"Flashcard Media with public_id={public_id} not found.")
        
        self.db_session.delete(model)