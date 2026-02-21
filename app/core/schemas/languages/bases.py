from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

ISOCode = Annotated[str, Field(min_length=2, max_length=2, pattern="^[a-z]{2}$")]

class LanguageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    iso_639_1: ISOCode