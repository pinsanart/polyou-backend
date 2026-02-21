from ....core.services.users.user_metadata import UserMetadataService
from ....infrastructure.repository.sqlalchemy.users.user_metadata import UserMetadataRepositorySQLAlchemy
from ....core.schemas.users.models import UserMetadata
from ....core.schemas.users.bases import UserMetadataBase
from ....core.exceptions.user import UserDoesNotExist

class UserMetadataServiceSQLAlchemy(UserMetadataService):
    def __init__(self, user_metadata_repository: UserMetadataRepositorySQLAlchemy):
        self.user_metadata_repository = user_metadata_repository
    
    def info(self, user_id: int) -> UserMetadata:
        user_metadata_model = self.user_metadata_repository.get(user_id)
        
        if not user_metadata_model:
            raise UserDoesNotExist(f"User with id={user_id} not found.")

        return UserMetadata.model_validate(user_metadata_model)
    
    def change(self, user_id: int, new_metadata: UserMetadataBase):
        user_metadata_model = self.user_metadata_repository.get(user_id)

        if not user_metadata_model:
            raise UserDoesNotExist(f"User with id={user_id} not found.")
        
        self.user_metadata_repository.update(user_id, new_metadata.model_dump(exclude_unset=True))