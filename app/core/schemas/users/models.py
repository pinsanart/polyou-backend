from .bases import (
    UserBase,
    UserCredentialsBase,
    UserMetadataBase,
    UserProfileBase,
    UserTargetLanguageBase,
    UserRefreshTokenBase
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

class UserRefreshToken(UserRefreshTokenBase):
    refresh_token_id: int
    user_id: int
    replaced_by: int | None = None