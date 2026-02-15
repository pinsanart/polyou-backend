from abc import ABC, abstractmethod

class FlashcardImagesRepository(ABC):
    @abstractmethod
    def update(self, id, new_images):
        pass