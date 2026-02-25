from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from .....core.repositories.auth.refresh_token import RefreshTokenRepository
from ....db.models import UserRefreshTokenModel

class RefreshTokenRepositorySQLAlchemy(RefreshTokenRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def get_by_id(self, id: int) -> UserRefreshTokenModel | None:
        return self.db_session.get(UserRefreshTokenModel, id)

    def get_by_hash(self, token_hash: str) -> UserRefreshTokenModel | None:
        stmt = select(UserRefreshTokenModel).where(UserRefreshTokenModel.token_hash == token_hash)
        return self.db_session.scalar(stmt)
    
    def get_by_user_id(self, user_id: int) -> List[UserRefreshTokenModel]:
        stmt = select(UserRefreshTokenModel).where(UserRefreshTokenModel.user_id == user_id)
        return self.db_session.scalars(stmt)
    
    def get_last_created_id(self, user_id: int) -> int | None:
        stmt = (
            select(UserRefreshTokenModel.refresh_token_id)
            .where(UserRefreshTokenModel.user_id == user_id)
            .order_by(UserRefreshTokenModel.created_at.desc())
            .limit(1)
        )
        return self.db_session.scalar(stmt)
    
    def create(self, user_refresh_token_model: UserRefreshTokenModel) -> None:
        self.db_session.add(user_refresh_token_model)

    def update(self, id: int, data: dict) -> None:
        user_refresh_token_model = self.db_session.get(UserRefreshTokenModel, id)

        if not user_refresh_token_model:
            raise ValueError(f"User Refresh Token with id={id} not found.")
        
        for key, value in data.items():
            if hasattr(user_refresh_token_model, key):
                setattr(user_refresh_token_model, key, value)