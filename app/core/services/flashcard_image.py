from abc import ABC, abstractmethod

class FlashcardImageService(ABC):
    @abstractmethod
    def update(self, user_id, public_id, new_images):
        pass