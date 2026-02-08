from abc import ABC, abstractmethod
from ..repositories.users import UsersRepository
from ..services.languages import LanguageService

class UserService(ABC):
    def __init__(self, users_repository:UsersRepository, language_service:LanguageService):
        self.users_repository = users_repository
        self.language_service = language_service

    @abstractmethod
    def register(self, register_information):
        pass