from ..factory import AppFactory

from ....mappers.flashcard_request import FlashcardRequestMapper
from ....mappers.flashcard_response import FlashcardResponseMapper

from ....services.sqlalchemy.flashcards.flashcard_type import FlashcardTypeServiceSQLAlchemy
from ....services.sqlalchemy.languages.language import LanguageServiceSQLAlchemy

@AppFactory.register(FlashcardRequestMapper)
def build_flashcard_request_mapper(factory: AppFactory):
    return FlashcardRequestMapper(
        flashcard_type_service= factory.create(FlashcardTypeServiceSQLAlchemy),
        language_service= factory.create(LanguageServiceSQLAlchemy)
    )

@AppFactory.register(FlashcardResponseMapper)
def build_flashcard_response_mapper(factory: AppFactory):
    return FlashcardResponseMapper(
        flashcard_type_service= factory.create(FlashcardTypeServiceSQLAlchemy),
        language_service= factory.create(LanguageServiceSQLAlchemy)
    )