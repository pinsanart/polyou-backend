from abc import ABC, abstractmethod
from typing import List

class FlashcardMediaRepository(ABC):
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_ids(self, ids: List):
        pass

    @abstractmethod
    def get_by_flashcard_id(self, flashcard_id):
        pass
    
    @abstractmethod
    def get_by_public_id(self, public_id):
        pass
    
    @abstractmethod
    def get_by_public_ids(self, public_ids: List):
        pass

    @abstractmethod
    def create_one(self, model):
        pass

    @abstractmethod
    def create_many(self, models: List):
        pass

    @abstractmethod
    def delete_one_by_id(self, id):
        pass

    @abstractmethod
    def delete_one_by_public_id(self, public_id):
        pass

    @abstractmethod
    def delete_many_by_ids(self, ids: List):
        pass

    @abstractmethod
    def delete_many_by_public_ids(self, public_ids: List):
        pass