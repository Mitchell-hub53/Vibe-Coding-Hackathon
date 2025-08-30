from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class RideStatus(str, Enum):
	scheduled = "scheduled"
	in_progress = "in_progress"
	completed = "completed"
	cancelled = "cancelled"


class RideCreate(BaseModel):
	child_id: int
	pickup_location: str
	dropoff_location: str
	scheduled_time: Optional[datetime] = None


class RideOut(BaseModel):
	id: int
	child_id: int
	pickup_location: str
	dropoff_location: str
	scheduled_time: Optional[datetime]
	status: RideStatus

	class Config:
		from_attributes = True


class IncidentStatus(str, Enum):
	open = "open"
	acknowledged = "acknowledged"
	resolved = "resolved"


class IncidentCreate(BaseModel):
	ride_id: Optional[int] = None
	child_id: Optional[int] = None
	driver_profile_id: Optional[int] = None
	vehicle_id: Optional[int] = None
	source: str
	latitude: Optional[float] = None
	longitude: Optional[float] = None
	snapshot_url: Optional[str] = None


class IncidentOut(BaseModel):
	id: int
	status: IncidentStatus
	source: str
	latitude: Optional[float]
	longitude: Optional[float]
	snapshot_url: Optional[str]
	created_at: datetime

	class Config:
		from_attributes = True