from abc import ABC, abstractmethod

class UserTargetLanguageService(ABC):
    @abstractmethod
    def add(self, user_id, target_language_add_info):
        pass

    @abstractmethod
    def remove(self, user_id, target_language_remove_info):
        pass

    @abstractmethod
    def list_user_languages_ids(self, user_id):
        pass