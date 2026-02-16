from abc import abstractmethod
from ..service import Service

class UserTargetLanguageService(Service):
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