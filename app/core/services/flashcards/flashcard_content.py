from abc import abstractmethod
from ..service import Service

class FlashcardContentService(Service):
    @abstractmethod
    def change(self, user_id, public_id, new_content):
        pass