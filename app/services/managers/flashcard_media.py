from uuid import UUID
from typing import BinaryIO

from ...core.exceptions.flashcards import PublicIDDoesNotBelongToUserError
from ...core.services.flashcards.flashcard_media import FlashcardMediaService
from ...core.services.users.user import UserService
from ...core.services.flashcards.flashcard import FlashcardService
from ...core.files_vault import FilesVault
from ...core.schemas.flashcards.bases import FlashcardMediaBase
from ...core.enums import MediaType, Fields

class FlashcardMediaManager:
    def __init__(self, flashcard_media_service:FlashcardMediaService, user_service:UserService, flashcard_service:FlashcardService, files_vault:FilesVault):
        self.flashcard_media_service    = flashcard_media_service
        self.user_service               = user_service
        self.flashcard_service          = flashcard_service
        self.files_vault                = files_vault

    def add(self, user_id: int, flashcard_public_id: UUID, field: Fields, media_type: MediaType, file_type:str, file_size:int, filename: str, file_stream: BinaryIO):
        user_public_id = self.user_service.get_public_id_by_id_or_fail(user_id)
        new_filename = self.files_vault.save(user_public_id, filename, file_stream)

        self.flashcard_media_service.add_one(
            flashcard_id= self.flashcard_service.get_id_by_public_id_or_fail(user_id, flashcard_public_id),
            media_info= FlashcardMediaBase(
                field=field,
                media_type= media_type,
                filename= new_filename,
                original_name= filename,
                file_type= file_type,
                file_size=file_size,
            )
        )
    
    def list_public_ids(self, user_id: int):
        return self.flashcard_media_service.list_public_ids_by_user_id(user_id)
    
    def delete(self, user_id: int, media_public_id: UUID):
        user_media_public_ids = self.flashcard_media_service.list_public_ids_by_user_id(user_id)
        if media_public_id not in user_media_public_ids:
            raise PublicIDDoesNotBelongToUserError(f"Media public id = '{media_public_id}' does not belong to the user.")
        
        user_public_id = self.user_service.get_public_id_by_id_or_fail(user_id)
        media_info = self.flashcard_media_service.info_by_public_id(media_public_id)

        self.flashcard_media_service.delete_one(media_public_id)
        self.files_vault.delete(user_public_id, media_info.filename)