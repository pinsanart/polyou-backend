from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from uuid import UUID
from typing import List

from .....core.repositories.flashcards.flashcard import FlashcardRepository
from ....db.models import FlashcardModel


class FlashcardRepositorySQLAlchemy(FlashcardRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _base_query_with_relations(self):
        return (
            select(FlashcardModel)
            .options(
                selectinload(FlashcardModel.sync_metadata),
                selectinload(FlashcardModel.content),
                selectinload(FlashcardModel.fsrs),
                selectinload(FlashcardModel.reviews),
                selectinload(FlashcardModel.images),
                selectinload(FlashcardModel.audios),
            )
        )
    
    def list_public_ids(self, user_id: int):
        stmt = select(FlashcardModel.public_id).where(
            FlashcardModel.user_id == user_id
        )
        return self.db_session.scalars(stmt).all()

    def list_ids(self, user_id: int) -> List[int]:
        stmt = select(FlashcardModel.flashcard_id).where(
            FlashcardModel.user_id == user_id
        )
        return self.db_session.scalars(stmt).all()

    def get_by_id(self, id: int) -> FlashcardModel | None:
        stmt = self._base_query_with_relations().where(
            FlashcardModel.flashcard_id == id
        )
        return self.db_session.execute(stmt).scalar_one_or_none()

    def get_by_public_id(self, public_id: UUID) -> FlashcardModel | None:
        stmt = self._base_query_with_relations().where(
            FlashcardModel.public_id == public_id
        )
        return self.db_session.execute(stmt).scalar_one_or_none()

    def list_by_ids(self, ids: List[int]) -> List[FlashcardModel]:
        stmt = self._base_query_with_relations().where(
            FlashcardModel.flashcard_id.in_(ids)
        )
        return self.db_session.scalars(stmt).all()

    def create_one(self, model: FlashcardModel) -> None:
        self.db_session.add(model)

    def create_many(self, models: List[FlashcardModel]) -> None:
        self.db_session.add_all(models)

    def delete_one(self, id: int) -> None:
        model = self.db_session.get(FlashcardModel, id)
        if model:
            self.db_session.delete(model)

    def delete_many(self, ids: List[int]) -> None:
        stmt = select(FlashcardModel).where(
            FlashcardModel.flashcard_id.in_(ids)
        )
        models = self.db_session.scalars(stmt).all()
        for model in models:
            self.db_session.delete(model)
