from fastapi_users import schemas
from uuid import UUID

# 사용자 정보 응답 시 사용될 스키마 (데이터베이스에서 클라이언트로 나갈 때)
class UserRead(schemas.BaseUser[UUID]):
    pass

# 사용자 등록 시 사용될 스키마 (클라이언트에서 서버로 들어올 때)
class UserCreate(schemas.BaseUserCreate):
    pass

# 사용자 정보 업데이트 시 사용될 스키마
class UserUpdate(schemas.BaseUserUpdate):
    pass