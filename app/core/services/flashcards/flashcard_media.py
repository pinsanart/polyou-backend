from abc import ABC, abstractmethod
from typing import List

class FlashcardMediaService(ABC):
    @abstractmethod
    def list_public_ids_by_user_id(self, user_id):
        pass

    @abstractmethod
    def list_public_ids_by_flashcard_id(self, flashcard_id):
        pass

    @abstractmethod
    def info_by_flashcard_id(self, flashcard_id):
        pass

    @abstractmethod
    def info_by_public_id(self, public_id):
        pass

    @abstractmethod
    def add_one(self, flashcard_id, media_info):
        pass

    @abstractmethod
    def add_many(self, flashcard_id, media_info: List):
        pass

    @abstractmethod
    def delete_one(self, public_id):
        pass

    @abstractmethod
    def delete_many(self, public_ids: List):
        pass