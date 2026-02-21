from abc import ABC, abstractmethod

class FlashcardService(ABC):
    @abstractmethod
    def get_id_by_public_id_or_fail(self, user_id, public_id):
        pass

    @abstractmethod
    def get_ids_by_public_ids_or_fail(self, user_id, public_ids):
        pass

    @abstractmethod
    def get_public_id_by_id_or_fail(self, user_id, id):
        pass

    @abstractmethod
    def get_public_ids_by_ids_or_fail(self, user_id, ids):
        pass

    @abstractmethod
    def list_public_ids(self, user_id):
        pass
    
    @abstractmethod
    def list_ids(self, user_id):
        pass

    @abstractmethod
    def create_one_from_request(self, user_id, flashcard_info):
        pass

    @abstractmethod
    def create_many_from_request(self, user_id, flashcards_info: list):
        pass
    
    @abstractmethod
    def delete_one(self, id):
        pass

    @abstractmethod
    def delete_many(self, ids):
        pass

    @abstractmethod
    def info_one(self, id):
        pass

    @abstractmethod
    def info_many(self, ids):
        pass