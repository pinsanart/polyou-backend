from typing import List
from uuid import UUID

from ....core.services.flashcards.flashcard import FlashcardService
from ....core.exceptions.flashcards import PublicIDAlreadyRegistedError, PublicIDDoesNotBelongToUserError, PublicIDDoesNotExistError
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard import FlashcardRepositorySQLAlchemy

from ....core.schemas.flashcards.models import Flashcard
from ....core.schemas.flashcards.requests import FlashcardCreateRequest

from ....mappers.flashcard_request import FlashcardRequestMapper

class FlashcardServiceSQLAlchemy(FlashcardService):
    def __init__(self, flashcard_repository: FlashcardRepositorySQLAlchemy, flashcard_request_mapper: FlashcardRequestMapper):
        self.flashcard_repository = flashcard_repository
        self.flashcard_request_mapper = flashcard_request_mapper
    
    def get_id_by_public_id_or_fail(self, user_id: int, public_id: UUID) -> int:
        flashcard_model = self.flashcard_repository.get_by_public_id(public_id)

        if not flashcard_model:
            raise PublicIDDoesNotExistError(f"Public ID '{public_id}' does not exist.")
        
        if flashcard_model.user_id != user_id:
            raise PublicIDDoesNotBelongToUserError(f"Public ID '{public_id}' does not belong to the authenticated user.")    

        return flashcard_model.flashcard_id
    
    def get_ids_by_public_ids_or_fail(self, user_id: int, public_ids: UUID) -> List[int]:
        ids = []

        for public_id in public_ids:
            flashcard_model = self.flashcard_repository.get_by_public_id(public_id)

            if not flashcard_model:
                raise PublicIDDoesNotExistError(f"Public ID '{public_id}' does not exist.")
        
            if flashcard_model.user_id != user_id:
                raise PublicIDDoesNotBelongToUserError(f"Public ID '{public_id}' does not belong to the authenticated user.")
            
            ids.append(flashcard_model.flashcard_id)

        return ids
    
    def get_public_id_by_id_or_fail(self, user_id: int, id: int):
        flashcard_model = self.flashcard_repository.get_by_id(id)

        if not flashcard_model:
            raise ValueError(f"ID '{id}' does not exist.")
        
        if flashcard_model.user_id != user_id:
            raise ValueError(f"ID '{id}' does not belong to the authenticated user.")
        
        return flashcard_model.public_id

    def get_public_ids_by_ids_or_fail(self, user_id, ids):
        public_ids = []

        for id in ids:
            flashcard_model = self.flashcard_repository.get_by_id(id)

            if not flashcard_model:
                raise ValueError(f"ID '{id}' does not exist.")
    
            if flashcard_model.user_id != user_id:
                raise ValueError(f"ID '{id}' does not belong to the authenticated user.")
            
            public_ids.append(flashcard_model.public_id)
        
        return public_ids
            
    def list_ids(self, user_id: int) -> List[int]:
        return self.flashcard_repository.list_ids(user_id)
    
    def list_public_ids(self, user_id: int) -> List[UUID]:
        ids = self.flashcard_repository.list_ids(user_id)

        public_ids = []
        for id in ids:
            model = self.flashcard_repository.get_by_id(id)
            public_ids.append(model.public_id)
        
        return public_ids
    
    def create_one_from_request(self, user_id: int, flashcard_info:FlashcardCreateRequest) -> UUID:
        flashcard_model = self.flashcard_repository.get_by_public_id(flashcard_info.public_id)

        if flashcard_model:
            raise PublicIDAlreadyRegistedError(f"Flashcard with public_id={flashcard_info.public_id} already exists.")

        flashcard_model = self.flashcard_request_mapper.request_to_db_model(user_id, flashcard_info)
        self.flashcard_repository.create_one(flashcard_model)
        return flashcard_model.public_id
    
    def create_many_from_request(self, user_id: int, flashcards_info: List[FlashcardCreateRequest]) -> List[UUID]:
        for info in flashcards_info:
            flashcard_model = self.flashcard_repository.get_by_public_id(info.public_id)

            if flashcard_model:
                raise PublicIDAlreadyRegistedError(f"Flashcard with public_id={info.public_id} already exists.")

        models = [
            self.flashcard_request_mapper.request_to_db_model(user_id, flashcard_info)
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