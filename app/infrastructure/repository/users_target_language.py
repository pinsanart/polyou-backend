from sqlalchemy.orm import Session
from sqlalchemy import delete, select

from ...core.repositories.users_target_languages import UsersTargetLanguagesRepository
from ..db.models import UserTargetLanguageModel

class UsersTargetLanguagesRepositoriesSQLAlchemy(UsersTargetLanguagesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, user_id, language_id) -> None:
        target_language = UserTargetLanguageModel(
            user_id = user_id,
            language_id= language_id
        )
        self.db_session.add(target_language)
        self.db_session.flush()

    def delete(self, user_id, language_id) -> None:
        stmt = delete(UserTargetLanguageModel).where(UserTargetLanguageModel.user_id == user_id, UserTargetLanguageModel.language_id == language_id)
        self.db_session.execute(stmt)

    def get(self, user_id, language_id) -> UserTargetLanguageModel | None:
        stmt = select(UserTargetLanguageModel).where(UserTargetLanguageModel.user_id == user_id, UserTargetLanguageModel.language_id == language_id)
        return self.db_session.execute(stmt).scalar_one_or_none()

    def list_user_target_languages_ids(self, user_id) -> list[int]:
        stmt = select(UserTargetLanguageModel.language_id).where(UserTargetLanguageModel.user_id == user_id)
        return list(self.db_session.execute(stmt).scalars().all())