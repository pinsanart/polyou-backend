from abc import abstractmethod
from ..service import Service

class FlashcardService(Service):
    @abstractmethod
    def create_one(self, user_id, flashcard_info):
        pass

    @abstractmethod
    def create_many(self, user_id, flashcards_info: list):
        pass
    
    @abstractmethod
    def list_public_ids(self, user_id):
        pass
    
    @abstractmethod
    def delete_one(self, user_id, public_id):
        pass

    @abstractmethod
    def delete_many(self, user_id, public_ids:list):
        pass

    @abstractmethod
    def info(self, user_id, public_ids:list):
        pass

    @abstractmethod
    def metadata(self, user_id, public_id):
        pass

    @abstractmethod
    def all_metadata(self, user_id):
        pass