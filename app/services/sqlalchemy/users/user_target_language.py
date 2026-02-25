from typing import List

from ....core.services.users.users_target_languages import UserTargetLanguageService
from ....infrastructure.repositories.sqlalchemy.users.user_target_language import UsersTargetLanguagesRepositorySQLAlchemy
from ....core.schemas.users.creates import UserTargetLanguageCreateInfo
from ....infrastructure.db.models import UserTargetLanguageModel
from ....core.exceptions.user_flashcard_target import TargetLanguageAlreadyExistsError

class UserTargetLanguageServiceSQLAlchemy(UserTargetLanguageService):
    def __init__(self, user_target_language_repository: UsersTargetLanguagesRepositorySQLAlchemy):
        self.user_target_language_repository = user_target_language_repository
    
    def add(self, user_id: int, target_language_add_info: UserTargetLanguageCreateInfo):
        model = self.user_target_language_repository.get(user_id, target_language_add_info.language_id)
        
        if model:
            raise TargetLanguageAlreadyExistsError("The user already has the target language added.")

        model = UserTargetLanguageModel(**target_language_add_info.model_dump(exclude_unset=True))
        self.user_target_language_repository.create(model)
    
    def remove(self, user_id, target_language_remove_info):
        pass

    def list_user_languages_ids(self, user_id: int) -> List[int]:
        return self.user_target_language_repository.list_user_target_languages_ids(user_id)
    