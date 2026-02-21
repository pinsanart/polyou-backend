from abc import ABC, abstractmethod

class FlashcardFSRSService(ABC):
    @abstractmethod
    def info(self, id):
        pass

    @abstractmethod
    def change(self, id, new_fsrs):
        pass