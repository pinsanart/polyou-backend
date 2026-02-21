from abc import ABC, abstractmethod

class UsersTargetLanguagesRepository(ABC):
    @abstractmethod
    def create(self, user_target_language_model):
        pass

    @abstractmethod
    def delete(self, user_id, language_id):
        pass

    @abstractmethod
    def get(self, user_id, language_id):
        pass

    @abstractmethod
    def list_user_target_languages_ids(self, user_id):
        pass
