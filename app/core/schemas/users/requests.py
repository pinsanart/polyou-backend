from pydantic import BaseModel, EmailStr
from ..languages.bases import ISOCode

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserTargetLanguageCreateRequest(BaseModel):
    iso_639_1: ISOCode