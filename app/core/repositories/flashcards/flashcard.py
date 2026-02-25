from abc import ABC, abstractmethod

class FlashcardRepository(ABC):
    @abstractmethod
    def list_ids(self, user_id):
        pass
    
    @abstractmethod
    def list_public_ids(self, user_id):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass
    
    @abstractmethod
    def get_by_ids(self, ids):
        pass
    
    @abstractmethod
    def get_by_public_id(self, public_id):
        pass

    @abstractmethod
    def get_by_public_ids(self, public_ids):
        pass
        
    @abstractmethod
    def create_one(self, model):
        pass

    @abstractmethod
    def create_many(self, models):
        pass

    @abstractmethod
    def delete_one(self, id):
        pass

    @abstractmethod
    def delete_many(self, ids):
        pass