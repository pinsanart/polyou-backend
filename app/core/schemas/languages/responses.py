from pydantic import BaseModel
from typing import List

from .bases import ISOCode

class AvailableLanguageResponse(BaseModel):
    available_languages: List[ISOCode]