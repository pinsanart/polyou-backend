# infrastructure/db/repositories/user_repository_sqlalchemy.py
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete

from ...core.repositories.users import UsersRepository
from ..db.models import UserModel

class UsersRepositorySQLAlchemy(UsersRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, entity: UserModel) -> UserModel:
        self.db_session.add(entity)
        self.db_session.flush()
        return entity

    def get_by_id(self, id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.user_id == id)
        return self.db_session.scalar(stmt)

    def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        return self.db_session.scalar(stmt)
    
    def update(self, id: int, data: dict) -> None:
        if not data:
            return 
        
        stmt = update(UserModel).where(UserModel.user_id == id).values(**data)
        self.db_session.execute(stmt)

    def delete(self, id: int) -> None:
        stmt = delete(UserModel).where(UserModel.user_id == id)
        self.db_session.execute(stmt)