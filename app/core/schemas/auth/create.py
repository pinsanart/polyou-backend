from pydantic import BaseModel
from uuid import UUID

class RefreshTokenCreateInfo(BaseModel):
    device_id: UUID
    device_name: str
    ip_address: str | None = None
    user_agent: str | None = None