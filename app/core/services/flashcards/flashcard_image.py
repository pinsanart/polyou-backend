from abc import abstractmethod
from ..service import Service

class FlashcardImageService(Service):
    @abstractmethod
    def update(self, user_id, public_id, new_images):
        pass