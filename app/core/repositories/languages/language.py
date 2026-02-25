from abc import ABC, abstractmethod

class LanguageRepository(ABC):
    @abstractmethod
    def list_ids(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_ids(self, ids):
        pass

    @abstractmethod
    def get_by_iso_639_1(self, iso_639_1):
        pass

    @abstractmethod
    def add(self, language_model):
        pass

    @abstractmethod
    def delete(self, id):
        pass