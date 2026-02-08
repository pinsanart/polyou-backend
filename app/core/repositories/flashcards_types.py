from abc import ABC, abstractmethod

class FlashcardTypesRepository(ABC):
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_name(self, name: str):
        pass