from abc import ABC, abstractmethod

class FlashcardImageService(ABC):
    @abstractmethod
    def info_all(self, flashcard_id):
        pass

    @abstractmethod
    def change(self, flashcard_id, new_images):
        pass