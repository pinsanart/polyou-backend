from abc import ABC, abstractmethod

class RefreshTokenService(ABC):
    @abstractmethod
    def rotate(self, user_id, expires_delta, user_refresh_token_info):
        pass
    
    @abstractmethod
    def validade(self, refresh_token):
        pass

    @abstractmethod
    def revoke_all_by_user(self, user_id):
        pass