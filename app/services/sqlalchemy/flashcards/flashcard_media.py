from typing import List
from uuid import UUID, uuid4

from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_media import FlashcardMediaRepositorySQLAlchemy
from ....infrastructure.db.models import FlashcardMediaModel
from ....core.services.flashcards.flashcard_media import FlashcardMediaService
from ....core.schemas.flashcards.models import FlashcardMedia
from ....core.schemas.flashcards.bases import FlashcardMediaBase
from ....core.exceptions.flashcards import PublicIDDoesNotExistError

class FlashcardMediaServiceSQLAlchemy(FlashcardMediaService):
    def __init__(self, flashcard_media_repository: FlashcardMediaRepositorySQLAlchemy):
        self.flashcard_media_repository = flashcard_media_repository

    def list_public_ids_by_user_id(self, user_id: int) -> List[UUID]:
        models = self.flashcard_media_repository.get_by_user_id(user_id)
        return [
            model.public_id 
            for model in models
        ]

    def list_public_ids_by_flashcard_id(self, flashcard_id: int) -> List[UUID]:
        models = self.flashcard_media_repository.get_by_flashcard_id(flashcard_id)
        return [
            model.public_id
            for model in models
        ]

    def info_by_flashcard_id(self, flashcard_id: int) -> FlashcardMedia:
        model = self.flashcard_media_repository.get_by_flashcard_id(flashcard_id)

        if not model:
            raise ValueError(f"Flashcard with id={flashcard_id} not found.")

        return FlashcardMedia.model_validate(model)

    def info_by_public_id(self, public_id: UUID) -> FlashcardMedia:
        model = self.flashcard_media_repository.get_by_public_id(public_id)

        if not model:
            raise PublicIDDoesNotExistError(f"Media public id ='{public_id}' not found.")

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
        try:
            self.flashcard_media_repository.delete_one_by_public_id(public_id)
        except:
            raise PublicIDDoesNotExistError(f"Media public id ='{public_id}' not found exist.") 

    def delete_many(self, public_ids: List[UUID]) -> None:
        try:
            self.flashcard_media_repository.delete_many_by_public_ids(public_ids)
        except:
            raise PublicIDDoesNotExistError(f"One or many media public ids were not found.")