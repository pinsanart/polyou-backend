from pydantic import BaseModel, EmailStr
from datetime import date

class UserTargetLanguagesCreateInfo(BaseModel):
    language_iso_639_1: str

class UserTargetLanguagesRemoveInfo(BaseModel):
    language_iso_639_1: str

class UserKnownLanguageCreateInfo(BaseModel):
    language_iso_639_1: str

class UserIdentity(BaseModel):
    user_id: int
    disabled: bool
    
class UserCredentials(BaseModel):
    email: EmailStr
    hashed_password: str

class UserProfile(BaseModel):
    first_name: str
    last_name: str
    birth: date | None = None

class UserLoginCredentials(BaseModel):
    email: EmailStr
    password: str

class UserRegisterInformation(BaseModel):
    credentials: UserLoginCredentials
    profile: UserProfile
    known_languages: list[UserKnownLanguageCreateInfo]