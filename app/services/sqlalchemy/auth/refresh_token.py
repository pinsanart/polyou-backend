from ....core.services.auth.refresh_token import RefreshTokenService
from ....core.security.refresh_token import generate_refresh_token, hash_token
from ....core.schemas.auth.create import RefreshTokenCreateInfo
from ....infrastructure.repository.sqlalchemy.auth.refresh_token import RefreshTokenRepositorySQLAlchemy
from ....mappers.user_sqlalchemy import UserSQLAlchemyMapper
from ....dependencies.time.utc_safe import utcnow
from datetime import timedelta

class RefreshTokenServiceSQLAlchemy(RefreshTokenService):
    def __init__(self, refresh_token_repository: RefreshTokenRepositorySQLAlchemy):
        self.refresh_token_repository = refresh_token_repository
    
    def create(self, user_id: int, expires_delta: timedelta, user_refresh_token_info: RefreshTokenCreateInfo) -> str:
        token = generate_refresh_token()
        token_hash = hash_token(token)
        expires_at = utcnow() + expires_delta
        device_id = user_refresh_token_info.device_id

        last_created_id = self.refresh_token_repository.get_last_created_id(user_id, device_id)
        
        model = UserSQLAlchemyMapper.refresh_token_create_to_model(user_id, token_hash, expires_at, user_refresh_token_info)
        self.refresh_token_repository.create(model)

        new_token_id = self.refresh_token_repository.get_last_created_id(user_id, device_id)

        if last_created_id is not None:
            self.refresh_token_repository.update(last_created_id, {'revoked': True, 'replaced_by': new_token_id})

        return token

    def info(self, id):
        pass

    def revoke(self, id):
        pass

    def revoke_all_by_user(self, user_id):
        pass