from abc import ABC, abstractmethod

from ...core.repositories.languages import LanguagesRepository

class LanguageService(ABC):
    def __init__(self, languages_repository:LanguagesRepository):
        self.languages_repository = languages_repository
    
    @abstractmethod
    def get_available(self) -> list[str]:
        pass

    @abstractmethod
    def get_id_by_iso_639_1_or_fail(self, iso_639_1:str) -> int:
        pass

    @abstractmethod
    def get_iso_639_1_by_id(self, id):
        pass