from ....infrastructure.repository.sqlalchemy.users.user import UserRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user_credentials import UserCredentialsRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user_metadata import UserMetadataRepositorySQLAlchemy
from ....core.schemas.users.requests import UserLoginRequest
from ....core.exceptions.auth import (
    InvalidCredentials,
    UserDisabled
)
from ....core.security.password import verify_password_hash
from ....core.services.auth.auth import AuthService

class AuthServiceSQLAlchemy(AuthService):
    def __init__(self, users_repository:UserRepositorySQLAlchemy, user_credentials_repository: UserCredentialsRepositorySQLAlchemy, user_metadata_repository: UserMetadataRepositorySQLAlchemy):
        self.users_repository = users_repository
        self.user_credentials_repository = user_credentials_repository
        self.user_metadata_repository = user_metadata_repository
    
    def authenticate_user(self, login_credentials:UserLoginRequest):
        email = login_credentials.email
        password = login_credentials.password

        user_model = self.users_repository.get_by_email(email)

        if not user_model:
            raise InvalidCredentials(f"Email '{email}' is not registered.")
        
        user_metadata_model = self.user_metadata_repository.get(user_model.user_id)

        if user_metadata_model.disabled:
            raise UserDisabled(f"Disabled User.")

        user_credentials_model = self.user_credentials_repository.get(user_model.user_id)

        if not verify_password_hash(password, user_credentials_model.hashed_password):
            raise InvalidCredentials("Wrong password.")
        
        return user_model.user_id