from abc import ABC, abstractmethod

class AuthService(ABC):
    @abstractmethod
    def authenticate_user(self, user_login_credentials):
        pass