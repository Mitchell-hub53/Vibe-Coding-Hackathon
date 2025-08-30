from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db_session
from app.db import models
from app.schemas.rides import RideCreate, RideOut, IncidentCreate, IncidentOut

router = APIRouter(prefix="/rides", tags=["rides"])


@router.post("/", response_model=RideOut)
def create_ride(payload: RideCreate, db: Session = Depends(get_db_session)):
	child = db.query(models.Child).filter(models.Child.id == payload.child_id).first()
	if not child:
		raise HTTPException(status_code=404, detail="Child not found")
	ride = models.Ride(
		child_id=payload.child_id,
		pickup_location=payload.pickup_location,
		dropoff_location=payload.dropoff_location,
		scheduled_time=payload.scheduled_time,
	)
	db.add(ride)
	db.commit()
	db.refresh(ride)
	return ride


@router.get("/", response_model=List[RideOut])
def list_rides(db: Session = Depends(get_db_session)):
	rides = db.query(models.Ride).order_by(models.Ride.created_at.desc()).all()
	return rides


@router.post("/incidents", response_model=IncidentOut)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db_session)):
	incident = models.Incident(
		ride_id=payload.ride_id,
		child_id=payload.child_id,
		driver_profile_id=payload.driver_profile_id,
		vehicle_id=payload.vehicle_id,
		source=payload.source,
		latitude=payload.latitude,
		longitude=payload.longitude,
		snapshot_url=payload.snapshot_url,
	)
	db.add(incident)
	db.commit()
	db.refresh(incident)
	return incident