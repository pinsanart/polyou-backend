from pydantic import BaseModel
from typing import List

from ..languages.bases import ISOCode

class UserIdentityResponse(BaseModel):
    user_id: int
    disabled: bool

class UserTargetLanguageResponse(BaseModel):
    user_target_languages: List[ISOCode]

class UserTargetLanguageCreateResponse(BaseModel):
    created_target_language: ISOCode