from sqlalchemy.orm import Session
from sqlalchemy import select

from .....core.repositories.users.user import UserRepository
from .....infrastructure.db.models import UserModel, UserCredentialsModel

class UserRepositorySQLAlchemy(UserRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, user_model: UserModel):
        self.db_session.add(user_model)

    def get_by_id(self, user_id: int) -> UserModel | None:
        return self.db_session.get(UserModel, user_id)

    def get_by_email(self, email:str) -> UserModel | None:
        stmt = (
            select(UserModel)
            .join(UserModel.credentials)
            .where(UserCredentialsModel.email == email)
        )
        return self.db_session.execute(stmt).scalar_one_or_none()
    
    def delete(self, user_id: int):
        model = self.db_session.get(UserModel, user_id)

        if not model:
            raise ValueError(f"User with id={user_id} nor found.")
        
        self.db_session.delete(model)