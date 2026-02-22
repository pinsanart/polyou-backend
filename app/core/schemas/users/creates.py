from pydantic import BaseModel, EmailStr
from uuid import UUID

from .models import (
    UserTargetLanguage,
)

from .bases import (
    UserProfileBase
)

class UserTargetLanguageCreateInfo(UserTargetLanguage):
    pass

class UserCredentialsCreateInfo(BaseModel):
    email: EmailStr
    password: str

class UserCreateInfo(BaseModel):
    credentials: UserCredentialsCreateInfo
    profile: UserProfileBase