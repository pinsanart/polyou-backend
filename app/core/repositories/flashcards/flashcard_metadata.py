from abc import ABC, abstractmethod

class FlashcardMetadataRepository(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def update(self, id, new_metadata):
        pass