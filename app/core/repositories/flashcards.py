from abc import ABC, abstractmethod

class FlashcardRepository(ABC):
    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def list_ids(self, user_id):
        pass
    
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_public_id(self, public_id):
        pass

    @abstractmethod
    def list_by_ids(self, ids):
        pass
    
    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass
