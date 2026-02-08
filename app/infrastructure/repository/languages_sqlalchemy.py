from sqlalchemy.orm import Session
from sqlalchemy import select

from ...core.repositories.languages import LanguagesRepository
from ...infrastructure.db.models import LanguageModel
from ..db.models import LanguageModel

class LanguageRepositorySQLAlchemy(LanguagesRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_ids(self) -> list[int]:
        stmt = select(LanguageModel.language_id)
        return list(self.db_session.execute(stmt).scalars().all())

    def get_by_id(self, id: int) -> LanguageModel:
        stmt = select(LanguageModel).where(LanguageModel.language_id == id)
        return self.db_session.scalar(stmt)

    def get_by_iso_639_1(self, iso_639_1:str) -> LanguageModel:
        stmt = select(LanguageModel).where(LanguageModel.iso_639_1 == iso_639_1)
        return self.db_session.scalar(stmt)