from ....core.services.users.user_credentials import UserCredentialsService
from ....infrastructure.repositories.sqlalchemy.users.user_credentials import UserCredentialsRepositorySQLAlchemy
from ....core.schemas.users.models import UserCredentials
from ....core.schemas.users.bases import UserCredentialsBase
from ....core.exceptions.user import UserDoesNotExist

class UserCredentialsServiceSQLAlchemy(UserCredentialsService):
    def __init__(self, user_credentials_repository: UserCredentialsRepositorySQLAlchemy):
        self.user_credentials_repository = user_credentials_repository
    
    def info(self, user_id: int) -> UserCredentials:
        user_credentials_model = self.user_credentials_repository.get(user_id)

        if not user_credentials_model:
            raise UserDoesNotExist(f"User with id={user_id} not found.")
        
        return UserCredentials.model_validate(user_credentials_model)

    def change(self, user_id: int, new_credentials: UserCredentialsBase):
        user_credentials_model = self.user_credentials_repository.get(user_id)

        if not user_credentials_model:
            raise UserDoesNotExist(f"User with id={user_id} not found.")
        
        self.user_credentials_repository.update(user_id, new_credentials.model_dump(exclude_unset=True))