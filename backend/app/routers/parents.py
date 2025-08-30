from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.db.base import get_db_session
from app.db import models
from app.core.deps import get_current_user_id

router = APIRouter(prefix="/parents", tags=["parents"]) 


class ChildCreate(BaseModel):
	full_name: str
	school_name: str | None = None
	class_level: str | None = None


class ChildOut(BaseModel):
	id: int
	full_name: str
	school_name: str | None
	class_level: str | None

	class Config:
		from_attributes = True


@router.get("/children", response_model=List[ChildOut])
def list_children(
	db: Session = Depends(get_db_session),
	user_id: int = Depends(get_current_user_id),
):
	parent = db.query(models.User).filter(models.User.id == user_id).first()
	if not parent:
		raise HTTPException(status_code=404, detail="Parent not found")
	return parent.children


@router.post("/children", response_model=ChildOut)
def create_child(
	payload: ChildCreate,
	db: Session = Depends(get_db_session),
	user_id: int = Depends(get_current_user_id),
):
	child = models.Child(
		full_name=payload.full_name,
		school_name=payload.school_name,
		class_level=payload.class_level,
		parent_id=user_id,
	)
	db.add(child)
	db.commit()
	db.refresh(child)
	return child