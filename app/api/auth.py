from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import async_session_maker
from app.repositories.user import UserRepository
from app.services.auth import AuthService
from app.schemes.user import UserCreate, UserInDB, Token, TokenData
from app.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_db():
    async with async_session_maker() as session:
        yield session


async def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)


async def get_auth_service(user_repository: UserRepository = Depends(get_user_repository)):
    return AuthService(user_repository)


@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, user_repository: UserRepository = Depends(get_user_repository), auth_service: AuthService = Depends(get_auth_service)):
    # Check if user already exists
    existing_user = await user_repository.get_by_username(user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_40_BAD_REQUEST,
            detail="Username already registered"
        )
    
    existing_email = await user_repository.get_by_email(user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_40_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    hashed_password = auth_service.get_password_hash(user.password)
    user.password = hashed_password
    
    # Create the user
    db_user = await user_repository.create(user)
    return db_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repository: UserRepository = Depends(get_user_repository), auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = auth_service.create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/profile", response_model=UserInDB)
async def read_profile(current_user: UserInDB = Depends(get_current_user)):
    return current_user