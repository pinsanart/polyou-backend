from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.languages.language import LanguageRepository
from .....infrastructure.db.models import LanguageModel

class LanguageRepositorySQLAlchemy(LanguageRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def list_ids(self) -> List[int]:
        stmt = select(LanguageModel.language_id)
        return self.db_session.scalars(stmt).all()
    
    def get_by_id(self, id: int) -> LanguageModel | None:
        return self.db_session.get(LanguageModel, id)

    def get_by_ids(self, ids: List[int]) -> List[LanguageModel]:
        stmt = select(LanguageModel).where(LanguageModel.language_id.in_(ids))
        return self.db_session.scalars(stmt).all()

    def get_by_iso_639_1(self, iso_639_1: str) -> LanguageModel | None:
        stmt = select(LanguageModel).where(LanguageModel.iso_639_1 == iso_639_1)
        return self.db_session.scalar(stmt)
    
    def add(self, language_model: LanguageModel) -> None:
        return self.db_session.add(language_model)
    
    def delete(self, id: int) -> None:
        model = self.db_session.get(LanguageModel, id)

        if not model:
            raise ValueError(f"Language with id={id} not found")
        
        self.db_session.delete(model)