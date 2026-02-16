from abc import abstractmethod
from ..service import Service

class LanguageService(Service):    
    @abstractmethod
    def get_available(self) -> list[str]:
        pass

    @abstractmethod
    def get_id_by_iso_639_1_or_fail(self, iso_639_1:str) -> int:
        pass

    @abstractmethod
    def get_iso_639_1_by_id(self, id):
        pass