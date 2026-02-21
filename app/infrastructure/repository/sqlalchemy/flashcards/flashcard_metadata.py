from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.flashcards.flashcard_metadata import FlashcardMetadataRepository
from .....infrastructure.db.models import FlashcardMetadataModel, FlashcardModel

class FlashcardMetadataRepositorySQLAlchemy(FlashcardMetadataRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_one(self, id: int) -> FlashcardMetadataModel | None:
        return self.db_session.get(FlashcardMetadataModel, id)

    def get_all(self, user_id: int) -> List[FlashcardMetadataModel]:
        stmt = (
            select(FlashcardMetadataModel)
            .join(FlashcardModel.server_metadata)
            .where(FlashcardModel.user_id == user_id)
        )
        return self.db_session.scalars(stmt).all()

    def update(self, id, data: dict) -> None:
        flashcard_metadata_model = self.db_session.get(FlashcardMetadataModel, id)

        if not flashcard_metadata_model:
            raise ValueError(f"Flashcard Metadata with id={id} not found.")

        for key, value in data.items():
            if hasattr(flashcard_metadata_model, key):
                setattr(flashcard_metadata_model, key, value)