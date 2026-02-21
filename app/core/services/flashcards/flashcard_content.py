from abc import ABC, abstractmethod

class FlashcardContentService(ABC):
    @abstractmethod
    def info(self, id):
        pass

    @abstractmethod
    def change(self, id, new_content):
        pass