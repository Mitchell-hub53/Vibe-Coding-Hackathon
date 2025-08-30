import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.config import settings
from app.db.base import Base
from app.db import models
from app.services.security import hash_password


def get_engine_url() -> str:
	# Prefer env DATABASE_URL; otherwise use configured SQLAlchemy URL
	return os.getenv("DATABASE_URL") or settings.sqlalchemy_database_uri


def seed():
	engine = create_engine(get_engine_url(), pool_pre_ping=True)
	Base.metadata.create_all(bind=engine)
	with Session(engine) as db:
		# Users
		parent = db.query(models.User).filter(models.User.email == "parent@safiri.com").first()
		if not parent:
			parent = models.User(
				email="parent@safiri.com",
				password_hash=hash_password("Parent123!"),
				full_name="Jane Parent",
				phone="+254700000001",
				role=models.UserRole.parent,
			)
			db.add(parent)

		driver_user = db.query(models.User).filter(models.User.email == "driver@safiri.com").first()
		if not driver_user:
			driver_user = models.User(
				email="driver@safiri.com",
				password_hash=hash_password("Driver123!"),
				full_name="John Driver",
				phone="+254700000002",
				role=models.UserRole.driver,
			)
			db.add(driver_user)
			db.flush()

		driver_profile = db.query(models.DriverProfile).filter(models.DriverProfile.user_id == driver_user.id).first()
		if not driver_profile:
			driver_profile = models.DriverProfile(
				user_id=driver_user.id,
				license_number="KDL-12345",
			)
			db.add(driver_profile)

		vehicle = db.query(models.Vehicle).filter(models.Vehicle.plate_number == "KDA 123A").first()
		if not vehicle:
			vehicle = models.Vehicle(
				driver_profile_id=driver_profile.id,
				plate_number="KDA 123A",
				camera_serial="CAM-0001",
				emergency_button_id="BTN-0001",
			)
			db.add(vehicle)

		db.flush()

		# Children
		child = (
			db.query(models.Child)
			.filter(models.Child.full_name == "Achieng Kemunto", models.Child.parent_id == parent.id)
			.first()
		)
		if not child:
			child = models.Child(
				full_name="Achieng Kemunto",
				school_name="St. Mary's",
				class_level="Grade 4",
				parent_id=parent.id,
			)
			db.add(child)
			db.flush()

		# Rides
		now = datetime.utcnow()
		r1 = models.Ride(
			child_id=child.id,
			pickup_location="Home",
			dropoff_location="St. Mary's",
			scheduled_time=now + timedelta(hours=12),
			status=models.RideStatus.scheduled,
			vehicle_id=vehicle.id,
			driver_profile_id=driver_profile.id,
		)
		r2 = models.Ride(
			child_id=child.id,
			pickup_location="St. Mary's",
			dropoff_location="Home",
			scheduled_time=now - timedelta(hours=4),
			status=models.RideStatus.completed,
			vehicle_id=vehicle.id,
			driver_profile_id=driver_profile.id,
		)
		db.add_all([r1, r2])
		db.flush()

		# Incident (open)
		incident = models.Incident(
			ride_id=r1.id,
			child_id=child.id,
			driver_profile_id=driver_profile.id,
			vehicle_id=vehicle.id,
			source="button",
			latitude=-1.2921,
			longitude=36.8219,
			snapshot_url="https://example.com/snapshots/demo.jpg",
		)
		db.add(incident)

		db.commit()
		print("Seed complete. Accounts:")
		print("  parent@safiri.com / Parent123!")
		print("  driver@safiri.com / Driver123!")


if __name__ == "__main__":
	seed()