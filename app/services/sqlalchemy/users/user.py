from ....core.services.users.user import UserService
from ....infrastructure.repositories.sqlalchemy.users.user import UserRepositorySQLAlchemy
from ....infrastructure.db.models import (
    UserModel,
    UserProfileModel,
    UserCredentialsModel,
    UserMetadataModel
)
from ....core.schemas.users.creates import UserCreateInfo
from ....core.security.password import hash_password
from ....core.exceptions.user import EmailAlreadyExistsError

class UserServiceSQLAlchemy(UserService):
    def __init__(self, user_repository: UserRepositorySQLAlchemy):
        self.user_repository = user_repository
    
    def _user_create_info_to_user_model(self, user_create_info: UserCreateInfo) -> UserModel:
        return (
            UserModel(
                credentials= (
                    UserCredentialsModel(
                        email = user_create_info.credentials.email,
                        hashed_password = hash_password(user_create_info.credentials.password)
                    )
                ),

                profile= (
                    UserProfileModel(
                        first_name= user_create_info.profile.first_name,
                        last_name= user_create_info.profile.last_name,
                        birth= user_create_info.profile.birth
                    )
                ),

                user_metadata= UserMetadataModel()
            )
        )

    def register(self, register_information: UserCreateInfo):
        email = register_information.credentials.email
        user_model = self.user_repository.get_by_email(email)

        if user_model:
            raise EmailAlreadyExistsError(f"Email '{email} already exists.'")

        user_model = self._user_create_info_to_user_model(register_information)
        self.user_repository.create(user_model)