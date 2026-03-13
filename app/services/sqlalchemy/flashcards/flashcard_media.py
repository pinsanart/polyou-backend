from typing import List
from uuid import UUID, uuid4

from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_media import FlashcardMediaRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardMediaModel
from ....core.services.flashcards.flashcard_media import FlashcardMediaService
from ....core.schemas.flashcards.models import FlashcardMedia
from ....core.schemas.flashcards.bases import FlashcardMediaBase

class FlashcardMediaServiceSQLAlchemy(FlashcardMediaService):
    def __init__(self, flashcard_media_repository: FlashcardMediaRepositorySQLAlchemy):
        self.flashcard_media_repository = flashcard_media_repository

    def list_public_ids(self, flashcard_id: int) -> List[UUID]:
        models = self.flashcard_media_repository.get_by_flashcard_id(flashcard_id)
        return [
            model.public_id
            for model in models
        ]

    def info(self, flashcard_id: int) -> FlashcardMedia:
        model = self.flashcard_media_repository.get_by_flashcard_id(flashcard_id)

        if not model:
            raise ValueError(f"Flashcard with id={flashcard_id} not found.")

        return FlashcardMedia.model_validate(model)

    def add_one(self, flashcard_id: int, media_info:FlashcardMediaBase) -> None:
        model = FlashcardMediaModel(
            flashcard_id = flashcard_id,
            public_id = uuid4(),
            **media_info.model_dump()
        )
        self.flashcard_media_repository.create_one(model)

    def add_many(self, flashcard_id:int, media_info: List[FlashcardMediaBase]) -> None:
        models = [
            FlashcardMediaModel(
                flashcard_id=flashcard_id,
                public_id = uuid4(),
                **m.model_dump()
            ) 
            for m in media_info
        ]
        self.flashcard_media_repository.create_many(models)

    def delete_one(self, public_id: UUID) -> None:
        self.flashcard_media_repository.delete_one_by_public_id(public_id)

    def delete_many(self, public_ids: List[UUID]) -> None:
        self.flashcard_media_repository.delete_many_by_public_ids(public_ids)