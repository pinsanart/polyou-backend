from abc import ABC, abstractmethod
from ..repositories.flashcards import FlashcardRepository
from ..services.flashcards_type import FlashcardTypesService
from ..services.users_target_languages import UserTargetLanguageService
from ..services.languages import LanguageService

class FlashcardService(ABC):
    def __init__(self, flashcards_repository:FlashcardRepository, user_target_language_service: UserTargetLanguageService, flashcard_types_service:FlashcardTypesService, language_service: LanguageService):
        self.flashcards_repository = flashcards_repository
        self.user_target_language_service = user_target_language_service
        self.flashcard_types_service = flashcard_types_service
        self.language_service = language_service

    @abstractmethod
    def create_one(self, user_id, flashcard_info):
        pass

    @abstractmethod
    def create_many(self, user_id, flashcards_info: list):
        pass
    
    @abstractmethod
    def list_public_ids(self, user_id):
        pass
    
    @abstractmethod
    def delete_one(self, user_id, public_id):
        pass

    @abstractmethod
    def delete_many(self, user_id, public_ids:list):
        pass

    @abstractmethod
    def info(self, user_id, public_ids:list):
        pass

    @abstractmethod
    def metadata(self, user_id, public_id):
        pass

    @abstractmethod
    def all_metadata(self, user_id):
        pass