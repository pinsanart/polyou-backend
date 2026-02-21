from typing import List
from uuid import UUID

from ....core.services.flashcards.flashcard import FlashcardService
from ....core.schemas.flashcards.creates import FlashcardCreateInfo
from ....core.exceptions.flashcards import PublicIDAlreadyRegistedError, PublicIDDoesNotBelongToUserError
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard import FlashcardRepositorySQLAlchemy
from ....mappers.flashcard_sqlalchemy import FlashcardSQLAlchemyMapper

from ....core.schemas.flashcards.models import Flashcard

class FlashcardServiceSQLAlchemy(FlashcardService):
    def __init__(self, flashcard_repository: FlashcardRepositorySQLAlchemy):
        self.flashcard_repository = flashcard_repository
    
    def get_id_by_public_id_or_fail(self, user_id: int, public_id: UUID) -> int:
        user_public_ids = self.flashcard_repository.list_public_ids(user_id)
        
        if public_id not in user_public_ids:
            raise PublicIDDoesNotBelongToUserError(f"Public ID '{public_id}' does not belong to the authenticated user.")    

        flashcard_model = self.flashcard_repository.get_by_public_id(public_id)

        return flashcard_model.flashcard_id
    
    def get_ids_by_public_ids_or_fail(self, user_id: int, public_ids: UUID) -> List[int]:
        user_public_ids = self.flashcard_repository.list_public_ids(user_id)

        for public_id in public_ids:
            if public_id not in user_public_ids:
                raise PublicIDDoesNotBelongToUserError(f"Public ID '{public_id}' does not belong to the authenticated user.")
        
        ids = [self.flashcard_repository.get_by_public_id(public_id).flashcard_id for public_id in public_ids]
        
        return ids
            
    def list_ids(self, user_id: int) -> List[int]:
        return self.flashcard_repository.list_ids(user_id)
    
    def list_public_ids(self, user_id: int) -> List[UUID]:
        ids = self.flashcard_repository.list_ids(user_id)

        public_ids = []
        for id in ids:
            model = self.flashcard_repository.get_by_id(id)
            public_ids.append(model.public_id)
        
        return public_ids
    
    def create_one(self, user_id: int, flashcard_info:FlashcardCreateInfo) -> UUID:
        flashcard_model = self.flashcard_repository.get_by_public_id(flashcard_info.public_id)

        if flashcard_model:
            raise PublicIDAlreadyRegistedError(f"Flashcard with public_id={flashcard_info.public_id} already exists.")

        flashcard_model = FlashcardSQLAlchemyMapper.to_model(user_id, flashcard_info)
        self.flashcard_repository.create_one(flashcard_model)
        return flashcard_model.public_id
    
    def create_many(self, user_id: int, flashcards_info: List[FlashcardCreateInfo]) -> List[UUID]:
        for info in flashcards_info:
            flashcard_model = self.flashcard_repository.get_by_public_id(info.public_id)

            if flashcard_model:
                raise PublicIDAlreadyRegistedError(f"Flashcard with public_id={info.public_id} already exists.")

        models = [
            FlashcardSQLAlchemyMapper.to_model(user_id, flashcard_info)
            for flashcard_info in flashcards_info
        ]

        self.flashcard_repository.create_many(models)

        public_ids = [
            model.public_id
            for model in models
        ]

        return public_ids

    def delete_one(self, id: int) -> None:
        self.flashcard_repository.delete_one(id)
    
    def delete_many(self, ids: List[int]) -> None:
        self.flashcard_repository.delete_many(ids)
    
    def info_one(self, id: int) -> Flashcard:
        model = self.flashcard_repository.get_by_id(id)
        return Flashcard.model_validate(model)
        
    def info_many(self, ids: List[int]) -> List[Flashcard]:
        models = [
            self.flashcard_repository.get_by_id(id)
            for id in ids
        ]

        infos = [
            Flashcard.model_validate(model)
            for model in models
        ]

        return infos