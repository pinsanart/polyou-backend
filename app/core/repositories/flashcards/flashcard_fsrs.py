from abc import ABC, abstractmethod

class FlashcardFSRSRepository(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def update(self, id, new_fsrs):
        pass