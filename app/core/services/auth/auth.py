from abc import abstractmethod
from ..service import Service

class AuthService(Service):
    @abstractmethod
    def authenticate_user(self, user_login_credentials):
        pass