from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id):
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def create(self, user_model):
        pass
    
    @abstractmethod
    def delete(self, user_id):
        pass