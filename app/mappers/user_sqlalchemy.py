from datetime import datetime

from ..core.schemas.auth.create import RefreshTokenCreateInfo
from ..infrastructure.db.models import RefreshTokenModel

class UserSQLAlchemyMapper:
    @staticmethod
    def refresh_token_create_to_model(user_id: int, token_hash: str, expires_at: datetime, create_info: RefreshTokenCreateInfo) -> RefreshTokenModel:
        return RefreshTokenModel(
            user_id = user_id,
            token_hash = token_hash,
            expires_at = expires_at,
            **create_info.model_dump()
        )