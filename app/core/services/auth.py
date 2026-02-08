from abc import ABC, abstractmethod
from ..repositories.users import UsersRepository 

class AuthService(ABC):
    def __init__(self, users_repository:UsersRepository):
        self.users_repository = users_repository

    @abstractmethod
    def authenticate_user(self, user_login_credentials):
        pass