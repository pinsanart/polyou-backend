from abc import ABC, abstractmethod

class FlashcardContentRepository(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def update(self, id, new_content):
        pass