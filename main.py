from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from uuid import UUID 
from fastapi_users import FastAPIUsers
from database import create_db_and_tables, User 
from users import get_user_manager, jwt_backend 
from schemas import UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager=get_user_manager,
    auth_backends=[jwt_backend],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application Startup: Connecting to DB and creating tables...")
    await create_db_and_tables() 
    yield
    print("Application Shutdown: Cleanup if necessary...")

app = FastAPI(
    title="Small But Steady - Coin Trading API",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    """루트 경로"""
    return {"status": "Service is running!", "version": "1.0.0"}

@app.get("/coin/price/{coin_id}", tags=["Coin Info"])
def get_coin_price(coin_id: str):
    """코인 가격 경로 (인증 불필요)"""
    return {"coin_id": coin_id, "가격": 100.0}

# --- FastAPI-Users 인증 라우터 등록 ---
# JWT 로그인/로그아웃 라우터 (POST /auth/jwt/login)
app.include_router(
    fastapi_users.get_auth_router(jwt_backend),
    prefix="/auth/jwt",
    tags=["Auth - Login"],
)

# 사용자 등록 라우터 (POST /auth/register)
app.include_router(
    fastapi_users.get_register_router(
        UserRead, 
        UserCreate
    ),
    prefix="/auth",
    tags=["Auth - Register"],
)

# 사용자 관리 라우터 (GET/PATCH/DELETE /users/me)
app.include_router(
    fastapi_users.get_users_router(
        UserRead, 
        UserUpdate                
    ), 
    prefix="/users",
    tags=["User Management"],
)

# --- 보호된 엔드포인트 ---
# 현재 활성화된 사용자만 접근 허용하는 의존성 주입
current_active_user = fastapi_users.current_user(active=True)

@app.get("/protected-route", tags=["examples"])
def protected_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello, {user.email}! Access granted."}