from pydantic import BaseModel, EmailStr
from uuid import UUID

class DeviceInfoRequest(BaseModel):
    device_id: UUID
    device_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str