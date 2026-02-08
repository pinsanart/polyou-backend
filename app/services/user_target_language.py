from ..core.services.users_target_languages import UserTargetLanguageService
from ..infrastructure.repository.users_target_language import UsersTargetLanguagesRepositoriesSQLAlchemy
from ..services.languages_sqlalchemy import LanguageServiceSQLAlchemy
from ..core.schemas.user import UserTargetLanguagesCreateInfo, UserTargetLanguagesRemoveInfo
from ..core.exceptions.user_flashcard_target import TargetLanguageAlreadyExistsError, NotAddedTargetLanguage

class UserTargetLanguageServiceSQLAlchemy(UserTargetLanguageService):
    def __init__(self, users_target_language_repository: UsersTargetLanguagesRepositoriesSQLAlchemy, language_service: LanguageServiceSQLAlchemy):
        super().__init__(users_target_language_repository, language_service)
    
    def add(self, user_id: int, target_language_add_info:UserTargetLanguagesCreateInfo) -> None:
        language_iso_639_1 = target_language_add_info.language_iso_639_1
        language_id = self.language_service.get_id_by_iso_639_1_or_fail(language_iso_639_1)

        target_language = self.user_target_language_repository.get(user_id, language_id)
        if target_language:
           raise TargetLanguageAlreadyExistsError(f"The user already has registered the language ISO 639-1 '{language_iso_639_1}'.")

        self.user_target_language_repository.insert(user_id, language_id)

    def remove(self, user_id, target_language_remove_info:UserTargetLanguagesRemoveInfo) -> None:
        language_iso_639_1 = target_language_remove_info.language_iso_639_1
        language_id = self.language_service.get_id_by_iso_639_1_or_fail(language_iso_639_1)
        self.user_target_language_repository.delete(user_id, language_id)

    def list_languages_iso_639_1(self, user_id):
        languages_ids = self.user_target_language_repository.list_user_target_languages_ids(user_id)
        languages_iso_639_1 = [
            self.language_service.get_iso_639_1_by_id(language_id)
            for language_id in languages_ids
        ]
        return languages_iso_639_1
    
    def get_user_language_id_by_iso_639_1(self, user_id: int, iso_639_1: str) -> int:
        if iso_639_1 not in self.list_languages_iso_639_1(user_id):
            raise NotAddedTargetLanguage(f"The user does not have the language ISO 639-1 '{iso_639_1}'added in his target languages.")
        language_id = self.language_service.get_id_by_iso_639_1_or_fail(iso_639_1)
        return language_id