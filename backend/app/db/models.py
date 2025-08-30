from datetime import datetime
from enum import Enum
from sqlalchemy import (
	Column,
	Integer,
	String,
	DateTime,
	Enum as SAEnum,
	ForeignKey,
	Text,
	Float,
	Boolean,
	Index,
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserRole(str, Enum):
	parent = "parent"
	driver = "driver"
	admin = "admin"


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(255), unique=True, nullable=False, index=True)
	password_hash = Column(String(255), nullable=False)
	full_name = Column(String(255), nullable=False)
	phone = Column(String(32), nullable=False, unique=True)
	role = Column(SAEnum(UserRole), default=UserRole.parent, nullable=False)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=datetime.utcnow)

	driver_profile = relationship("DriverProfile", uselist=False, back_populates="user")
	children = relationship("Child", back_populates="parent")


class Child(Base):
	__tablename__ = "children"

	id = Column(Integer, primary_key=True)
	full_name = Column(String(255), nullable=False)
	school_name = Column(String(255), nullable=True)
	class_level = Column(String(64), nullable=True)
	parent_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

	parent = relationship("User", back_populates="children")
	rides = relationship("Ride", back_populates="child")


class DriverProfile(Base):
	__tablename__ = "driver_profiles"

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
	license_number = Column(String(64), nullable=True)
	verified_at = Column(DateTime, nullable=True)

	user = relationship("User", back_populates="driver_profile")
	vehicles = relationship("Vehicle", back_populates="driver_profile")
	rides = relationship("Ride", back_populates="driver_profile")


class Vehicle(Base):
	__tablename__ = "vehicles"

	id = Column(Integer, primary_key=True)
	driver_profile_id = Column(Integer, ForeignKey("driver_profiles.id"), nullable=False)
	plate_number = Column(String(32), unique=True, nullable=False)
	camera_serial = Column(String(64), nullable=True)
	emergency_button_id = Column(String(64), unique=True, nullable=True)

	driver_profile = relationship("DriverProfile", back_populates="vehicles")
	rides = relationship("Ride", back_populates="vehicle")


class RideStatus(str, Enum):
	scheduled = "scheduled"
	in_progress = "in_progress"
	completed = "completed"
	cancelled = "cancelled"


class Ride(Base):
	__tablename__ = "rides"

	id = Column(Integer, primary_key=True)
	child_id = Column(Integer, ForeignKey("children.id"), nullable=False, index=True)
	driver_profile_id = Column(Integer, ForeignKey("driver_profiles.id"), nullable=True)
	vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)

	pickup_location = Column(String(255), nullable=False)
	dropoff_location = Column(String(255), nullable=False)
	scheduled_time = Column(DateTime, nullable=True)
	status = Column(SAEnum(RideStatus), default=RideStatus.scheduled, nullable=False)

	created_at = Column(DateTime, default=datetime.utcnow)

	child = relationship("Child", back_populates="rides")
	driver_profile = relationship("DriverProfile", back_populates="rides")
	vehicle = relationship("Vehicle", back_populates="rides")
	events = relationship("RideEvent", back_populates="ride")


class RideEventType(str, Enum):
	start = "start"
	location_update = "location_update"
	stop = "stop"
	emergency = "emergency"


class RideEvent(Base):
	__tablename__ = "ride_events"

	id = Column(Integer, primary_key=True)
	ride_id = Column(Integer, ForeignKey("rides.id"), index=True, nullable=False)
	event_type = Column(SAEnum(RideEventType), nullable=False)
	timestamp = Column(DateTime, default=datetime.utcnow)
	latitude = Column(Float, nullable=True)
	longitude = Column(Float, nullable=True)
	notes = Column(Text, nullable=True)

	ride = relationship("Ride", back_populates="events")


class IncidentStatus(str, Enum):
	open = "open"
	acknowledged = "acknowledged"
	resolved = "resolved"


class Incident(Base):
	__tablename__ = "incidents"

	id = Column(Integer, primary_key=True)
	ride_id = Column(Integer, ForeignKey("rides.id"), nullable=True)
	child_id = Column(Integer, ForeignKey("children.id"), nullable=True)
	driver_profile_id = Column(Integer, ForeignKey("driver_profiles.id"), nullable=True)
	vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
	source = Column(String(32), nullable=False)  # button, driver_app, system
	latitude = Column(Float, nullable=True)
	longitude = Column(Float, nullable=True)
	snapshot_url = Column(String(512), nullable=True)
	status = Column(SAEnum(IncidentStatus), default=IncidentStatus.open, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

	__table_args__ = (
		Index("ix_incidents_created_at", "created_at"),
	)