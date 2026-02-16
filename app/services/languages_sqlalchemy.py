from ..core.services.languages.languages import LanguageService
from ..infrastructure.repository.languages_sqlalchemy import LanguageRepositorySQLAlchemy
from ..core.exceptions.languages import LanguageNotAvailableError

class LanguageServiceSQLAlchemy(LanguageService):
    def __init__(self, languages_repository:LanguageRepositorySQLAlchemy):
        self.languages_repository = languages_repository
    
    def get_available(self) -> list[str]:
        language_ids = self.languages_repository.list_ids()
        
        languages_iso_639_1 = []
        for language_id in language_ids:
            language_model = self.languages_repository.get_by_id(language_id)
            iso_639_1 = language_model.iso_639_1
            languages_iso_639_1.append(iso_639_1)
        
        return languages_iso_639_1
    
    def get_id_by_iso_639_1_or_fail(self, iso_639_1:str) -> bool:
        language = self.languages_repository.get_by_iso_639_1(iso_639_1)
        if not language:
            raise LanguageNotAvailableError(f"The language ISO 639-1 '{iso_639_1}' is not available.")
        return language.language_id
        
    def get_iso_639_1_by_id(self, id: int) -> str:
        language = self.languages_repository.get_by_id(id)
        return language.iso_639_1