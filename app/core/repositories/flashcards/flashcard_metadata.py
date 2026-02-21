from abc import ABC, abstractmethod

class FlashcardMetadataRepository(ABC):
    @abstractmethod
    def get_one(self, id):
        pass
    
    @abstractmethod
    def get_all(self, user_id):
        pass

    @abstractmethod
    def update(self, id, data):
        pass