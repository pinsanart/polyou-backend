from ..infrastructure.repository.users_sqlalchemy import UsersRepositorySQLAlchemy
from ..core.schemas.user import UserLoginCredentials
from ..core.exceptions.auth import (
    InvalidCredentials,
    UserDisabled
)
from ..core.security.password import verify_password_hash
from ..core.services.auth.auth import AuthService

class AuthServiceSQLAlchemy(AuthService):
    def __init__(self, users_repository:UsersRepositorySQLAlchemy):
        self.users_repository = users_repository
    
    def authenticate_user(self, login_credentials:UserLoginCredentials):
        login_email = login_credentials.email
        login_password = login_credentials.password

        user = self.users_repository.get_by_email(login_email)

        if not user:
            raise InvalidCredentials(f"The email '{login_email}' is not registered.")
        
        if user.disabled:
            raise UserDisabled(f"The email '{login_email}' is disabled.")
        
        if not verify_password_hash(login_password, user.hashed_password):
            raise InvalidCredentials("Wrong password.")
        
        return user.user_id