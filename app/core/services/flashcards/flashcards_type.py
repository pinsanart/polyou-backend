from abc import abstractmethod

from ..service import Service

class FlashcardTypesService(Service):
    @abstractmethod
    def get_id_by_name_or_fail(self, name:str):
        pass

    @abstractmethod
    def get_name_by_id(self, id):
        pass