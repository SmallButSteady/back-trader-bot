import os
from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

# database.py에서 정의된 User 모델과 get_async_session 함수를 가져옵니다.
from database import User, get_async_session 

from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

# .env 파일에서 SECRET 키를 로드합니다.
SECRET = os.environ.get("SECRET")

class UserManager(BaseUserManager[User, UUID]):
    """사용자 관리 로직을 처리하는 클래스"""
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """DB 세션을 받아 사용자 DB 어댑터를 제공합니다."""
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """사용자 DB 어댑터를 받아 사용자 관리자(UserManager)를 제공합니다."""
    yield UserManager(user_db)


# --- JWT 토큰 인증 백엔드 정의 ---
# 1. Bearer Transport (토큰을 헤더로 전달)
bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

# 2. JWT Strategy (토큰 유효 시간 정의)
def get_jwt_strategy() -> JWTStrategy:
    """토큰 유효 시간 1시간"""
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

# 3. Authentication Backend (최종 인증 시스템)
jwt_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)