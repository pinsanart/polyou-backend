from abc import ABC, abstractmethod

class FlashcardContentRepository(ABC):
    @abstractmethod
    def update(self, id, new_content):
        pass