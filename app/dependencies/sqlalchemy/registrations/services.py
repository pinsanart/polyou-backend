from ..factory                                                  import AppFactory

from ....infrastructure.repository.flashcard_content_sqlalchemy import FlashcardContentRepositorySQLAlchemy
from ....infrastructure.repository.flashcard_fsrs_sqlalchemy    import FlashcardFSRSRepositorySQLAlchemy
from ....infrastructure.repository.flashcard_image_sqlalchemy   import FlashcardImagesRepositorySQLAlchemy
from ....infrastructure.repository.flashcards_sqlalchemy        import FlashcardRepositorySQLAlchemy
from ....infrastructure.repository.flashcards_type_sqlalchemy   import FlashcardTypesRepositorySQLAlchemy
from ....infrastructure.repository.languages_sqlalchemy         import LanguageRepositorySQLAlchemy
from ....infrastructure.repository.users_sqlalchemy             import UsersRepositorySQLAlchemy
from ....infrastructure.repository.users_target_language        import UsersTargetLanguagesRepositoriesSQLAlchemy

from ....services.auth_sqlalchemy                               import AuthServiceSQLAlchemy
from ....services.users_sqlalchemy                              import UserServiceSQLAlchemy
from ....services.languages_sqlalchemy                          import LanguageServiceSQLAlchemy
from ....services.flascards_types_sqlalchemy                    import FlashcardsTypesServiceSQLAlchemy
from ....services.flashcard_content_sqlalchemy                  import FlashcardContentServiceSQLAlchemy
from ....services.flashcards_sqlalchemy                         import FlashcardServiceSQLAlchemy
from ....services.user_target_language                          import UserTargetLanguageServiceSQLAlchemy
from ....services.flashcard_image_sqlalchemy                    import FlashcardImageServiceSQLAlchemy
from ....services.flashcard_fsrs_sqlalchemy                     import FlashcardFSRSServiceSQLAlchemy

@AppFactory.register(AuthServiceSQLAlchemy)
def build_auth_service(factory: AppFactory):
    return AuthServiceSQLAlchemy(
        users_repository= factory.create(UsersRepositorySQLAlchemy)
    )

@AppFactory.register(LanguageServiceSQLAlchemy)
def build_language_service(factory: AppFactory):
    return LanguageServiceSQLAlchemy(
        languages_repository= factory.create(LanguageRepositorySQLAlchemy)        
    )

@AppFactory.register(UserServiceSQLAlchemy)
def build_user_service(factory: AppFactory):
    return UserServiceSQLAlchemy(
        users_repository= factory.create(UsersRepositorySQLAlchemy),
        language_service= factory.create(LanguageServiceSQLAlchemy)
    )

@AppFactory.register(FlashcardsTypesServiceSQLAlchemy)
def build_flashcard_type_service(factory: AppFactory):
    return FlashcardsTypesServiceSQLAlchemy(
        flashcards_types_repository= factory.create(FlashcardTypesRepositorySQLAlchemy)
    )

@AppFactory.register(UserTargetLanguageServiceSQLAlchemy)
def build_user_target_language_service(factory: AppFactory):
    return UserTargetLanguageServiceSQLAlchemy(
        users_target_language_repository =  factory.create(UsersTargetLanguagesRepositoriesSQLAlchemy),
        language_service=                   factory.create(LanguageServiceSQLAlchemy)
    )

@AppFactory.register(FlashcardServiceSQLAlchemy)
def build_flashcard_service(factory: AppFactory):
    return FlashcardServiceSQLAlchemy(
        flashcards_repository=          factory.create(FlashcardRepositorySQLAlchemy),
        user_target_language_service=   factory.create(UserTargetLanguageServiceSQLAlchemy),
        flashcard_type_service=         factory.create(FlashcardsTypesServiceSQLAlchemy),
        language_service=               factory.create(LanguageServiceSQLAlchemy)
    )

@AppFactory.register(FlashcardContentServiceSQLAlchemy)
def build_flashcard_content_service(factory: AppFactory):
    return FlashcardContentServiceSQLAlchemy(
        flashcard_content_repository=   factory.create(FlashcardContentRepositorySQLAlchemy),
        flashcard_service=              factory.create(FlashcardServiceSQLAlchemy)
    )

@AppFactory.register(FlashcardImageServiceSQLAlchemy)
def build_flashcard_image_service(factory: AppFactory):
    return FlashcardImageServiceSQLAlchemy(
        flashcard_image_repository=     factory.create(FlashcardImagesRepositorySQLAlchemy),
        flashcard_service=              factory.create(FlashcardServiceSQLAlchemy)
    )

@AppFactory.register(FlashcardFSRSServiceSQLAlchemy)
def build_flashcard_fsrs_service(factory: AppFactory):
    return FlashcardFSRSServiceSQLAlchemy(
        flashcard_fsrs_repository=  factory.create(FlashcardFSRSRepositorySQLAlchemy),
        flashcard_service=          factory.create(FlashcardServiceSQLAlchemy)
    )