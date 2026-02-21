from ..factory                                                                  import AppFactory

from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_content     import FlashcardContentRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_fsrs        import FlashcardFSRSRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_image       import FlashcardImageRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard             import FlashcardRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_type        import FlashcardTypeRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.flashcards.flashcard_metadata    import FlashcardMetadataRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.languages.language               import LanguageRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user_target_language       import UsersTargetLanguagesRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user                       import UserRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user_credentials           import UserCredentialsRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user_metadata              import UserMetadataRepositorySQLAlchemy
from ....infrastructure.repository.sqlalchemy.users.user_profile               import UserProfileRepositorySQLAlchemy

from ....services.sqlalchemy.auth.auth                                          import AuthServiceSQLAlchemy
from ....services.sqlalchemy.users.user_target_language                         import UserTargetLanguageServiceSQLAlchemy
from ....services.sqlalchemy.users.user                                         import UserServiceSQLAlchemy
from ....services.sqlalchemy.users.user_credentials                             import UserCredentialsServiceSQLAlchemy
from ....services.sqlalchemy.users.user_metadata                                import UserMetadataServiceSQLAlchemy
from ....services.sqlalchemy.users.user_profile                                 import UserProfileServiceSQLAlchemy
from ....services.sqlalchemy.flashcards.flashcard                               import FlashcardServiceSQLAlchemy
from ....services.sqlalchemy.flashcards.flashcard_content                       import FlashcardContentServiceSQLAlchemy                  
from ....services.sqlalchemy.flashcards.flashcard_fsrs                          import FlashcardFSRSServiceSQLAlchemy
from ....services.sqlalchemy.flashcards.flashcard_image                         import FlashcadImageServiceSQLAlchemy
from ....services.sqlalchemy.flashcards.flashcard_type                          import FlashcardTypeServiceSQLAlchemy
from ....services.sqlalchemy.flashcards.flashcard_metadata                      import FlashcardMetadataServiceSQLAlchemy
from ....services.sqlalchemy.languages.language                                 import LanguageServiceSQLAlchemy

from ....mappers.flashcard_request                                              import FlashcardRequestMapper

@AppFactory.register(UserCredentialsServiceSQLAlchemy)
def build_user_credentials_service(factory: AppFactory):
    return UserCredentialsServiceSQLAlchemy(
        user_credentials_repository= factory.create(UserCredentialsRepositorySQLAlchemy)
    )

@AppFactory.register(UserProfileServiceSQLAlchemy)
def build_user_profile_service(factory: AppFactory):
    return UserProfileServiceSQLAlchemy(
        user_profile_repository= factory.create(UserProfileRepositorySQLAlchemy)
    )

@AppFactory.register(UserMetadataServiceSQLAlchemy)
def build_user_metadata_service(factory: AppFactory):
    return UserMetadataServiceSQLAlchemy(
        user_metadata_repository= factory.create(UserMetadataRepositorySQLAlchemy)
    )

@AppFactory.register(AuthServiceSQLAlchemy)
def build_auth_service(factory: AppFactory):
    return AuthServiceSQLAlchemy(
        users_repository= factory.create(UserRepositorySQLAlchemy),
        user_credentials_repository= factory.create(UserCredentialsRepositorySQLAlchemy),
        user_metadata_repository= factory.create(UserMetadataRepositorySQLAlchemy)
    )

@AppFactory.register(UserTargetLanguageServiceSQLAlchemy)
def build_user_target_language_service(factory: AppFactory):
    return UserTargetLanguageServiceSQLAlchemy(
        user_target_language_repository= factory.create(UsersTargetLanguagesRepositorySQLAlchemy)
    )

@AppFactory.register(UserServiceSQLAlchemy)
def build_user_service(factory: AppFactory):
    return UserServiceSQLAlchemy(
        user_repository= factory.create(UserRepositorySQLAlchemy)
    )

@AppFactory.register(FlashcardServiceSQLAlchemy)
def build_flashcard_service(factory: AppFactory):
    return FlashcardServiceSQLAlchemy(
        flashcard_repository= factory.create(FlashcardRepositorySQLAlchemy),
        flashcard_request_mapper= factory.create(FlashcardRequestMapper)
    )

@AppFactory.register(FlashcardContentServiceSQLAlchemy)
def build_flashcard_content_service(factory: AppFactory):
    return FlashcardContentServiceSQLAlchemy(
        flashcard_content_repository=factory.create(FlashcardContentRepositorySQLAlchemy)
    )

@AppFactory.register(FlashcardFSRSServiceSQLAlchemy)
def build_flashcard_fsrs_service(factory: AppFactory):
    return FlashcardFSRSServiceSQLAlchemy(
        flashcard_fsrs_repository= factory.create(FlashcardFSRSRepositorySQLAlchemy)
    )

@AppFactory.register(FlashcadImageServiceSQLAlchemy)
def build_flashcard_image_service(factory: AppFactory):
    return FlashcadImageServiceSQLAlchemy(
        flashcard_image_repository= factory.create(FlashcardImageRepositorySQLAlchemy)
    )

@AppFactory.register(FlashcardTypeServiceSQLAlchemy)
def build_flashcard_type_service(factory: AppFactory):
    return FlashcardTypeServiceSQLAlchemy(
        flashcard_type_repository= factory.create(FlashcardTypeRepositorySQLAlchemy)
    )

@AppFactory.register(LanguageServiceSQLAlchemy)
def build_language_service(factory: AppFactory):
    return LanguageServiceSQLAlchemy(
        language_repository= factory.create(LanguageRepositorySQLAlchemy)
    )

@AppFactory.register(FlashcardMetadataServiceSQLAlchemy)
def build_flashcard_metadata_service(factory: AppFactory):
    return FlashcardMetadataServiceSQLAlchemy(
        flashcard_metadata_repository= factory.create(FlashcardMetadataRepositorySQLAlchemy)
    )