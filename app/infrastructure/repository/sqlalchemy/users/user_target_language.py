from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.users.user_target_language import UsersTargetLanguagesRepository
from .....infrastructure.db.models import UserTargetLanguageModel

class UsersTargetLanguagesRepositorySQLAlchemy(UsersTargetLanguagesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def create(self, user_target_language_model: UserTargetLanguageModel) -> None:
        self.db_session.add(user_target_language_model)
    
    def delete(self, user_id: int, language_id: int) -> None:
        stmt = select(UserTargetLanguageModel).where(UserTargetLanguageModel.language_id == language_id, UserTargetLanguageModel.user_id == user_id)
        
        db_model = self.db_session.scalar(stmt)

        if not db_model:
            raise ValueError(f"Language where user_id={user_id} and language_id={language_id} not found.")
        
        self.db_session.delete(db_model)
    
    def get(self, user_id: int, language_id: int) -> UserTargetLanguageModel | None:
        stmt = select(UserTargetLanguageModel).where(UserTargetLanguageModel.language_id == language_id, UserTargetLanguageModel.user_id == user_id)
        return self.db_session.scalar(stmt)

    def list_user_target_languages_ids(self, user_id: int) -> List[int]:
        stmt = select(UserTargetLanguageModel.language_id).where(UserTargetLanguageModel.user_id == user_id)
        return self.db_session.scalars(stmt).all()