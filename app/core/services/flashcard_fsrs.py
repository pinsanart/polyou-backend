from abc import ABC, abstractmethod

class FlashcardFSRSService(ABC):
    @abstractmethod
    def change(self, user_id, public_id, new_fsrs):
        pass