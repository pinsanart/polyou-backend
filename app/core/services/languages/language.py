from abc import ABC, abstractmethod

class LanguageService(ABC):    
    @abstractmethod
    def get_available_languages_iso_639_1(self) -> list[str]:
        pass

    @abstractmethod
    def get_id_by_iso_639_1_or_fail(self, iso_639_1:str) -> int:
        pass

    @abstractmethod
    def get_iso_639_1_by_id_or_fail(self, id):
        pass

    @abstractmethod
    def create(self, language_info):
        pass

    @abstractmethod
    def delete(self, id):
        pass