from ....core.services.users.user_profile import UserProfileService
from ....infrastructure.repository.sqlalchemy.users.user_profile import UserProfileRepositorySQLAlchemy
from ....core.schemas.users.models import User
from ....core.schemas.users.bases import UserBase
from ....core.exceptions.user import UserDoesNotExist

class UserProfileServiceSQLAlchemy(UserProfileService):
    def __init__(self, user_profile_repository: UserProfileRepositorySQLAlchemy):
        self.user_profile_repository = user_profile_repository
    
    def info(self, user_id: int) -> User:
        user_model = self.user_profile_repository.get(user_id)

        if not user_model:
            raise UserDoesNotExist(f"User with id={user_id} not found.")
        
        return User.model_validate(user_model)

    def change(self, user_id: int, new_metadata: UserBase):
        user_model = self.user_profile_repository.get(user_id)

        if not user_model:
            raise UserDoesNotExist(f"User with id={user_id} not found.")
        
        self.user_profile_repository.update(user_id, new_metadata.model_dump(exclude_unset=True))