from abc import ABC, abstractmethod

class FlashcardContentService(ABC):
    @abstractmethod
    def change(self, user_id, public_id, new_content):
        pass