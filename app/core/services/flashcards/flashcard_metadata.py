from abc import ABC, abstractmethod

class FlashcardMetadataService(ABC):
    @abstractmethod
    def info_one(self, id):
        pass

    def info_all(self, user_id):
        pass

    @abstractmethod
    def change(self, id, new_metadata):
        pass