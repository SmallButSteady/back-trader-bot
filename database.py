import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID 

# --- 1단계: 환경 변수 로드 및 확인 ---
print("--- DB SETUP LOG START ---")
print("1. [STEP 1] .env 파일 로드 시도...")
load_dotenv() 

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL 환경 변수가 없습니다. .env 파일을 확인하세요.")
else:
    # 보안상 비밀번호를 제거하고 출력
    safe_url = DATABASE_URL.split('@')[0] + '@' + DATABASE_URL.split('@')[1].split('/')[0] + '/...'
    print(f"✅ SUCCESS: DATABASE_URL 로드 완료. (연결 정보: {safe_url})")


# --- 2단계: SQLAlchemy 기본 설정 ---

class Base(DeclarativeBase):
    """모든 SQLAlchemy 모델이 상속받을 기본 클래스입니다."""
    pass

try:
    print("2. [STEP 2] DB 엔진 생성 시도...")
    engine = create_async_engine(DATABASE_URL)
    print("✅ SUCCESS: 비동기 DB 엔진 객체 생성 완료.")
except Exception as e:
    print(f"❌ ERROR: DB 엔진 생성 실패 (DATABASE_URL 형식 오류 가능성). 내용: {e}")

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
print("3. [STEP 3] 비동기 세션 팩토리 생성 완료.")


# --- 3단계: FastAPI-Users 모델 정의 ---

class User(SQLAlchemyBaseUserTableUUID, Base):
    """trader-bot 스키마에 매핑되는 사용자 모델"""
    __table_args__ = {"schema": "trader-bot"} 
    print(f"4. [STEP 4] User 모델 정의 완료. 목표 스키마: {__table_args__['schema']}")
    pass


# --- 4단계: DB 세션 의존성 함수 ---

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

# --- 5단계: DB 테이블 초기화 함수 ---

async def create_db_and_tables():
    print("5. [STEP 5] create_db_and_tables 함수 실행 시작...")
    try:
        async with engine.begin() as conn:
            print("6. [STEP 6] DB 연결 성공! 테이블 생성 명령 실행...")
            # Base.metadata에 등록된 모든 테이블(User 포함)을 생성 시도
            await conn.run_sync(Base.metadata.create_all)
            print("✅ SUCCESS: 테이블 생성 명령 실행 완료. (권한 오류가 없다면 테이블 생성됨)")
    except Exception as e:
        print(f"❌ FATAL ERROR: 테이블 생성 중 심각한 오류 발생. 내용: {e.__class__.__name__}: {e}")
        print("해결: PostgreSQL 서버의 권한 또는 스키마 존재 여부를 DBeaver로 확인하세요.")
    print("--- DB SETUP LOG END ---")