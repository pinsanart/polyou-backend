from abc import ABC, abstractmethod
from ..repositories.users_target_languages import UsersTargetLanguagesRepository
from .languages import LanguageService

class UserTargetLanguageService(ABC):
    def __init__(self, users_target_language_repository: UsersTargetLanguagesRepository, language_service: LanguageService):
        self.user_target_language_repository = users_target_language_repository
        self.language_service = language_service

    @abstractmethod
    def add(self, user_id, target_language_add_info):
        pass

    @abstractmethod
    def remove(self, user_id, target_language_remove_info):
        pass

    @abstractmethod
    def list_languages_iso_639_1(self, user_id):
        pass

    @abstractmethod
    def get_user_language_id_by_iso_639_1(self, user_id, iso_639_1):
        pass