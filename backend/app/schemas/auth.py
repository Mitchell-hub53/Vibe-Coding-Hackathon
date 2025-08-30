from pydantic import BaseModel, EmailStr
from enum import Enum


class UserRole(str, Enum):
	parent = "parent"
	driver = "driver"
	admin = "admin"


class UserCreate(BaseModel):
	email: EmailStr
	password: str
	full_name: str
	phone: str
	role: UserRole = UserRole.parent


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"


class UserOut(BaseModel):
	id: int
	email: EmailStr
	full_name: str
	phone: str
	role: UserRole

	class Config:
		from_attributes = True