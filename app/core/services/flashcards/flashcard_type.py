from abc import ABC, abstractmethod

class FlashcardTypeService(ABC):
    @abstractmethod
    def get_id_by_name_or_fail(self, name:str):
        pass

    @abstractmethod
    def get_name_by_id_or_fail(self, id):
        pass

    @abstractmethod
    def add(self, flashcard_type_info):
        pass

    @abstractmethod
    def delete(self, id):
        pass