from abc import ABC, abstractmethod

class LanguagesRepository(ABC):
    @abstractmethod
    def list_ids(self):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_iso_639_1(self, iso_639_1):
        pass