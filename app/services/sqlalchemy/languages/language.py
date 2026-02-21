from typing import List

from ....core.exceptions.languages import LanguageNotAvailableError
from ....core.services.languages.language import LanguageService
from ....infrastructure.repository.sqlalchemy.languages.language import LanguageRepositorySQLAlchemy
from ....infrastructure.db.models import LanguageModel
from ....core.schemas.languages.creates import LanguageCreateInfo

class LanguageServiceSQLAlchemy(LanguageService):
    def __init__(self, language_repository: LanguageRepositorySQLAlchemy):
        self.language_repository = language_repository
    
    def get_available_languages_iso_639_1(self) -> List[str]:
        ids = self.language_repository.list_ids()
        languages_iso_639_1 = []
        for id in ids:
            model = self.language_repository.get_by_id(id)
            languages_iso_639_1.append(model.iso_639_1)
        return languages_iso_639_1

    def get_id_by_iso_639_1_or_fail(self, iso_639_1: str) -> int:
        language_model = self.language_repository.get_by_iso_639_1(iso_639_1)
        if not language_model:
            raise LanguageNotAvailableError(f"Language with 'ISO 639-1'={iso_639_1} not found.")
        return language_model.language_id

    def get_iso_639_1_by_id_or_fail(self, id: int) -> str:
        language_model = self.language_repository.get_by_id(id)
        if not language_model:
            raise LanguageNotAvailableError(f"Language with id={id} not found.")
        return language_model.iso_639_1
    
    def create(self, language_info: LanguageCreateInfo) -> None:
        language_model = LanguageModel(
            name = language_info.name,
            iso_639_1= language_info.iso_639_1
        )
        self.language_repository.add(language_model)

    def delete(self, id: int) -> None:
        language_model = self.language_repository.get_by_id(id)
        if not language_model:
            raise LanguageNotAvailableError(f"Language with id={id} not found.")
        self.language_repository.delete(id)