from abc import ABC, abstractmethod
from ..repositories.flashcards_types import FlashcardTypesRepository

class FlashcardTypesService(ABC):
    def __init__(self, flashcards_types_repository:FlashcardTypesRepository):
        self.flashcards_types_repository = flashcards_types_repository

    @abstractmethod
    def get_id_by_name_or_fail(self, name:str):
        pass

    @abstractmethod
    def get_name_by_id(self, id):
        pass