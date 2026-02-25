from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID

from .....core.repositories.auth.refresh_token import RefreshTokenRepository
from ....db.models import RefreshTokenModel

class RefreshTokenRepositorySQLAlchemy(RefreshTokenRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_by_id(self, id: int) -> RefreshTokenModel | None:
        return self.db_session.get(RefreshTokenModel, id)

    def get_by_hash(self, token_hash: str) -> RefreshTokenModel | None:
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        return self.db_session.scalar(stmt)
    
    def get_by_user_id(self, user_id: int) -> List[RefreshTokenModel]:
        stmt = select(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id)
        return self.db_session.scalars(stmt)
    
    def get_last_created_id(self, user_id: int, device_id: UUID) -> int | None:
        stmt = (
            select(RefreshTokenModel.refresh_token_id)
            .where(RefreshTokenModel.user_id == user_id, RefreshTokenModel.device_id == device_id)
            .order_by(RefreshTokenModel.created_at.desc())
            .limit(1)
        )
        return self.db_session.scalar(stmt)
    
    def create(self, user_refresh_token_model: RefreshTokenModel) -> None:
        self.db_session.add(user_refresh_token_model)

    def update(self, id: int, data: dict) -> None:
        user_refresh_token_model = self.db_session.get(RefreshTokenModel, id)

        if not user_refresh_token_model:
            raise ValueError(f"User Refresh Token with id={id} not found.")
        
        for key, value in data.items():
            if hasattr(user_refresh_token_model, key):
                setattr(user_refresh_token_model, key, value)