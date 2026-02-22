from abc import ABC, abstractmethod

class UserRefreshTokenRepository(ABC):
    @abstractmethod
    def create(self, user_refresh_token_model):
        pass
    
    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def get_by_hash(self, token_hash):
        pass

    @abstractmethod
    def get_by_user_id(self, user_id):
        pass

    @abstractmethod
    def update(self, id, data):
        pass