from abc import ABC, abstractmethod
from typing import List

class FlashcardMediaService(ABC):
    @abstractmethod
    def list_public_ids(self, flashcard_id):
        pass

    @abstractmethod
    def info(self, flashcard_id):
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