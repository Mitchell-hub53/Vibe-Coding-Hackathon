from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.db.base import get_db_session
from app.db import models
from app.schemas.auth import UserCreate, UserLogin, UserOut, Token
from app.services.security import hash_password, verify_password, create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register_user(payload: UserCreate, db: Session = Depends(get_db_session)):
	existing = db.query(models.User).filter(models.User.email == payload.email).first()
	if existing:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = models.User(
		email=payload.email,
		password_hash=hash_password(payload.password),
		full_name=payload.full_name,
		phone=payload.phone,
		role=models.UserRole(payload.role.value),
	)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db_session)):
	user = db.query(models.User).filter(models.User.email == payload.email).first()
	if not user or not verify_password(payload.password, user.password_hash):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
	token = create_access_token(str(user.id))
	return Token(access_token=token)