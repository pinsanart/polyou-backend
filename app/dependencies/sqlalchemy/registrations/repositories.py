from ..factory                                                                      import AppFactory

from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_content          import FlashcardContentRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_fsrs             import FlashcardFSRSRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_image            import FlashcardImageRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard                  import FlashcardRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_type             import FlashcardTypeRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_sync_metadata    import FlashcardSyncMetadataRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_review           import FlashcardReviewRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.flashcards.flashcard_audio            import FlashcardAudioRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.languages.language                    import LanguageRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.users.user_target_language            import UsersTargetLanguagesRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.users.user                            import UserRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.users.user_credentials                import UserCredentialsRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.users.user_metadata                   import UserMetadataRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.users.user_profile                    import UserProfileRepositorySQLAlchemy
from ....infrastructure.repositories.sqlalchemy.auth.refresh_token                    import RefreshTokenRepositorySQLAlchemy

@AppFactory.register(FlashcardContentRepositorySQLAlchemy)
def build_flashcard_content_repository(factory: AppFactory):
    return FlashcardContentRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardAudioRepositorySQLAlchemy)
def build_flashcard_audio_repository(factory: AppFactory):
    return FlashcardAudioRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardFSRSRepositorySQLAlchemy)
def build_flashcard_fsrs_repository(factory: AppFactory):
    return FlashcardFSRSRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardImageRepositorySQLAlchemy)
def build_flashcard_image_repository(factory: AppFactory):
    return FlashcardImageRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardReviewRepositorySQLAlchemy)
def build_flashcard_review_repository(factory: AppFactory):
    return FlashcardReviewRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardRepositorySQLAlchemy)
def build_flashcard_repository(factory: AppFactory):
    return FlashcardRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardTypeRepositorySQLAlchemy)
def build_flashcard_type_repository(factory: AppFactory):
    return FlashcardTypeRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(FlashcardSyncMetadataRepositorySQLAlchemy)
def build_flashcard_sync_metadata_repository(factory: AppFactory):
    return FlashcardSyncMetadataRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(LanguageRepositorySQLAlchemy)
def build_language_repository(factory: AppFactory):
    return LanguageRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UserRepositorySQLAlchemy)
def build_user_repository(factory: AppFactory):
    return UserRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UsersTargetLanguagesRepositorySQLAlchemy)
def build_user_target_language_repository(factory: AppFactory):
    return UsersTargetLanguagesRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UserCredentialsRepositorySQLAlchemy)
def build_user_credentials_repository(factory: AppFactory):
    return UserCredentialsRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UserMetadataRepositorySQLAlchemy)
def build_user_metadata_repository(factory: AppFactory):
    return UserMetadataRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(UserProfileRepositorySQLAlchemy)
def build_user_profile_repository(factory: AppFactory):
    return UserProfileRepositorySQLAlchemy(factory.container.db)

@AppFactory.register(RefreshTokenRepositorySQLAlchemy)
def build_user_refresh_token_repository(factory: AppFactory):
    return RefreshTokenRepositorySQLAlchemy(factory.container.db)