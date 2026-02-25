from sqlalchemy.orm import Session
from .....core.repositories.users.user_profile import UserProfileRepository
from .....infrastructure.db.models import UserProfileModel

class UserProfileRepositorySQLAlchemy(UserProfileRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get(self, user_id: int) -> UserProfileModel | None:
        return self.db_session.get(UserProfileModel, user_id)
    
    def update(self, user_id: int, data: dict):
        user_profile_model = self.db_session.get(UserProfileModel, user_id)

        if not user_profile_model:
            raise ValueError(f"User with id={user_id} not found.")
        
        for key, value in data.items():
            if hasattr(user_profile_model, key):
                setattr(user_profile_model, key, value)