from pydantic import BaseModel
from typing import List
from uuid import UUID

from .bases import (
    FlashcardBase,
    FlashcardSyncMetadataBase
)

from .requests import (
    FlashcardPatchContentRequest,
    FlashcardPatchFSRSRequest,
    FlashcardPatchImagesRequest,
    FlashcardPatchReviewsRequest,
    FlashcardPatchAudiosRequest,
    FlashcardPatchSyncMetadataRequest
)

from ..languages.bases import ISOCode

class FlashcardGetResponse(BaseModel):
    public_ids: List[UUID]

class FlashcardInfoResponse(FlashcardBase):
    flashcard_type_name: str
    language_iso_639_1: ISOCode

class FlashcardGetInfosResponse(BaseModel):
    infos: List[FlashcardInfoResponse]

class FlashcardGetSyncMetadataResponse(BaseModel):
    public_id: UUID
    sync_metadata: FlashcardSyncMetadataBase

class FlashcardGetAllSyncMetadataResponse(BaseModel):
    public_ids: List[UUID]
    sync_metadatas: List[FlashcardGetSyncMetadataResponse]

class FlashcardPostResponse(BaseModel):
    public_id: UUID

class FlashcardPostBatchResponse(BaseModel):
    public_ids: List[UUID]

class FlashcardPatchContentResponse(FlashcardPatchContentRequest):
    pass

class FlashcardPatchFSRSResponse(FlashcardPatchFSRSRequest):
    pass

class FlashcardPatchImagesResponse(FlashcardPatchImagesRequest):
    pass

class FlashcardPatchReviewsResponse(FlashcardPatchReviewsRequest):
    pass

class FlashcardPatchAudiosResponse(FlashcardPatchAudiosRequest):
    pass

class FlashcardPatchSyncMetadataResponse(FlashcardPatchSyncMetadataRequest):
    pass

class FlashcardDeleteResponse(BaseModel):
    deleted_public_id: UUID

class FlashcardDeleteBatchResponse(BaseModel):
    deleted_public_ids: List[UUID]