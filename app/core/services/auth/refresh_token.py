from abc import ABC, abstractmethod

class RefreshTokenService(ABC):
    @abstractmethod
    def create(self, user_id, user_refresh_token_info):
        pass
    
    @abstractmethod
    def info(self, id):
        pass

    @abstractmethod
    def revoke(self, id):
        pass

    @abstractmethod
    def revoke_all_by_user(self, user_id):
        pass