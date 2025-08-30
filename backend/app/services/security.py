from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
	return password_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
	return password_context.verify(plain_password, password_hash)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
	if expires_minutes is None:
		expires_minutes = settings.access_token_expire_minutes
	expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
	to_encode = {"sub": subject, "exp": expire}
	return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)