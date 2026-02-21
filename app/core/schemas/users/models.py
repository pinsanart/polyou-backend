from .bases import (
    UserBase,
    UserCredentialsBase,
    UserMetadataBase,
    UserProfileBase,
    UserTargetLanguageBase
)

class UserCredentials(UserCredentialsBase):
    user_id: int

class User(UserBase):
    user_id: int

class UserMetadata(UserMetadataBase):
    user_id: int

class UserProfile(UserProfileBase):
    user_id: int

class UserTargetLanguage(UserTargetLanguageBase):
    user_id: int
    language_id: int