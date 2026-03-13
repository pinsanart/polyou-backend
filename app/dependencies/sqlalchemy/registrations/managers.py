from ..factory import AppFactory

from ....services.managers.flashcard_media import FlashcardMediaManager
from ....services.sqlalchemy.flashcards.flashcard_media import FlashcardMediaServiceSQLAlchemy
from ....services.sqlalchemy.users.user import UserServiceSQLAlchemy
from ....services.sqlalchemy.flashcards.flashcard import FlashcardServiceSQLAlchemy
from ....core.files_vault import FilesVault

from ....core.config.config import settings

@AppFactory.register(FlashcardMediaManager)
def build_flashcard_media_manager(factory: AppFactory):
    return FlashcardMediaManager(
        flashcard_media_service= factory.create(FlashcardMediaServiceSQLAlchemy),
        user_service= factory.create(UserServiceSQLAlchemy),
        flashcard_service= factory.create(FlashcardServiceSQLAlchemy),
        files_vault= FilesVault(settings.USERS_MEDIA_PATH),
    )