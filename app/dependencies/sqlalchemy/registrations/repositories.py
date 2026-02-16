from ..factory                                                      import AppFactory

from ....infrastructure.repository.flashcard_content_sqlalchemy     import FlashcardContentRepositorySQLAlchemy
from ....infrastructure.repository.flashcard_fsrs_sqlalchemy        import FlashcardFSRSRepositorySQLAlchemy
from ....infrastructure.repository.flashcard_image_sqlalchemy       import FlashcardImagesRepositorySQLAlchemy
from ....infrastructure.repository.flashcards_sqlalchemy            import FlashcardRepositorySQLAlchemy
from ....infrastructure.repository.flashcards_type_sqlalchemy       import FlashcardTypesRepositorySQLAlchemy
from ....infrastructure.repository.languages_sqlalchemy             import LanguageRepositorySQLAlchemy
from ....infrastructure.repository.users_sqlalchemy                 import UsersRepositorySQLAlchemy
from ....infrastructure.repository.users_target_language            import UsersTargetLanguagesRepositoriesSQLAlchemy

@AppFactory.register(FlashcardContentRepositorySQLAlchemy)
def build_flashcard_content_repository(factory: AppFactory):
    return FlashcardContentRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardFSRSRepositorySQLAlchemy)
def build_flashcard_fsrs_repository(factory: AppFactory):
    return FlashcardFSRSRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardImagesRepositorySQLAlchemy)
def build_flashcard_image_repository(factory: AppFactory):
    return FlashcardImagesRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardRepositorySQLAlchemy)
def build_flashcard_repository(factory: AppFactory):
    return FlashcardRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardTypesRepositorySQLAlchemy)
def build_flashcard_type_repository(factory: AppFactory):
    return FlashcardTypesRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(LanguageRepositorySQLAlchemy)
def build_language_repository(factory: AppFactory):
    return LanguageRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UsersRepositorySQLAlchemy)
def build_user_repository(factory: AppFactory):
    return UsersRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UsersTargetLanguagesRepositoriesSQLAlchemy)
def build_user_target_language_repository(factory: AppFactory):
    return UsersTargetLanguagesRepositoriesSQLAlchemy(factory.container.db)