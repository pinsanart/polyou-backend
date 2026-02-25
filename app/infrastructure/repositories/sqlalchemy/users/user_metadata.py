from sqlalchemy.orm import Session

from .....core.repositories.users.user_metadata import UserMetadataRepository
from .....infrastructure.db.models import UserMetadataModel

class UserMetadataRepositorySQLAlchemy(UserMetadataRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, user_id: int) -> UserMetadataModel | None:
        return self.db_session.get(UserMetadataModel, user_id)

    def update(self, user_id: int, data: dict):
        user_metadata_model = self.db_session.get(UserMetadataModel, user_id)

        if not user_metadata_model:
            raise ValueError(f"User with id={user_id} not found.")
        
        for key, value in data.items():
            if hasattr(user_metadata_model, key):
                setattr(user_metadata_model, key, value)