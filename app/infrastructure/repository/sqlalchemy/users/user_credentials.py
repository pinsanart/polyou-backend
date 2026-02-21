from sqlalchemy.orm import Session
from .....core.repositories.users.user_credentials import UserCredentialsRepository
from .....infrastructure.db.models import UserCredentialsModel

class UserCredentialsRepositorySQLAlchemy(UserCredentialsRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get(self, user_id: int) -> UserCredentialsModel | None:
        return self.db_session.get(UserCredentialsModel, user_id)
    
    def update(self, user_id: int, data: dict):
        user_credentials_model = self.db_session.get(UserCredentialsModel, user_id)

        if not user_credentials_model:
            raise ValueError(f"User with id={user_id} not found.")
        
        for key, value in data.items():
            if hasattr(user_credentials_model, key):
                setattr(user_credentials_model, key, value)