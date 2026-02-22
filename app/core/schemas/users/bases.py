from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from uuid import UUID

from ....dependencies.time.utc_safe import utcnow

class UserTargetLanguageBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    pass

class UserProfileBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    birth: date

class UserMetadataBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disabled: bool = False
    created_at: datetime = utcnow
    updated_at: datetime = utcnow

class UserCredentialsBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    hashed_password: str
    

class UserRefreshTokenBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token_hash: str
    device_id: UUID
    device_name: str
    ip_address: str | None = None
    user_agent: str | None = None
    expires_at: datetime
    revoked: bool
    created_at: datetime = utcnow

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    credentials: UserCredentialsBase
    user_metadata: UserMetadataBase
    profile: UserProfileBase
