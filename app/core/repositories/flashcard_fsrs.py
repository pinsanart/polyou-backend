from abc import ABC, abstractmethod

class FlashcardFSRSRepository(ABC):
    @abstractmethod
    def update(self, id, new_fsrs):
        pass