from ..core.services.users import UserService
from ..infrastructure.repository.users_sqlalchemy import UsersRepositorySQLAlchemy
from ..core.exceptions.user import EmailAlreadyExistsError
from ..core.security.password import hash_password
from .languages_sqlalchemy import LanguageServiceSQLAlchemy

from ..core.schemas.user import (
    UserRegisterInformation
)

from ..infrastructure.db.models import (
    UserModel,
    UserProfileModel,
    UserKnownLanguageModel,
)

class UserServiceSQLAlchemy(UserService):
    def __init__(self, users_repository: UsersRepositorySQLAlchemy, language_service: LanguageServiceSQLAlchemy):
        super().__init__(users_repository, language_service)
    
    def register(self, register_information:UserRegisterInformation) -> int:
        email = register_information.credentials.email

        user = self.users_repository.get_by_email(email)
        if user:
            raise EmailAlreadyExistsError(f"The email '{email}' already exists.")
        
        password = register_information.credentials.password
        hashed_password = hash_password(password)

        profile = UserProfileModel(
            first_name = register_information.profile.first_name,
            last_name = register_information.profile.last_name,
            birth = register_information.profile.birth
        )

        known_languages = register_information.known_languages
        
        languages_ids = []
        for known_language in known_languages:
            iso_639_1 = known_language.language_iso_639_1
            language_id = self.language_service.get_id_by_iso_639_1_or_fail(iso_639_1)
            languages_ids.append(language_id)

        known_languages = [
            UserKnownLanguageModel(
                language_id = language_id
            )
            for language_id in languages_ids
        ]

        user = UserModel(
            email = email,
            hashed_password = hashed_password,
            profile = profile,
            known_languages = known_languages
        )

        user = self.users_repository.create(user)
        return user.user_id