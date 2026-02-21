from abc import ABC, abstractmethod

class FlashcardTypeRepository(ABC):
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_name(self, name: str):
        pass

    @abstractmethod
    def create(self, new_type):
        pass

    @abstractmethod
    def delete(self, id):
        pass