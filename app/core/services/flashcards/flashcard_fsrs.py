from abc import abstractmethod
from ..service import Service

class FlashcardFSRSService(Service):
    @abstractmethod
    def change(self, user_id, public_id, new_fsrs):
        pass