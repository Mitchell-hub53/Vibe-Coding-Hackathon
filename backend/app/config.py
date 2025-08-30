from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import field_validator


class Settings(BaseSettings):
	app_name: str = "SafiriSchola API"
	environment: str = "development"
	api_v1_prefix: str = "/api/v1"

	# Security
	jwt_secret_key: str = "change-me"
	jwt_algorithm: str = "HS256"
	access_token_expire_minutes: int = 60 * 24

	# Databases
	database_url: Optional[str] = None
	mysql_user: str = "safiri"
	mysql_password: str = "safiri"
	mysql_host: str = "mysql"
	mysql_port: int = 3306
	mysql_db: str = "safiri"

	mongodb_uri: str = "mongodb://mongo:27017"
	mongodb_db: str = "safiri"

	# Integrations
	africastalking_username: Optional[str] = None
	africastalking_api_key: Optional[str] = None

	mpesa_consumer_key: Optional[str] = None
	mpesa_consumer_secret: Optional[str] = None

	cors_origins: list[str] = [
		"http://localhost:5173",
		"http://127.0.0.1:5173",
		"http://localhost:3000",
	]

	@field_validator("cors_origins", mode="before")
	@classmethod
	def parse_cors(cls, v):
		if isinstance(v, str):
			return [o.strip() for o in v.split(",") if o.strip()]
		return v

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"

	@property
	def sqlalchemy_database_uri(self) -> str:
		if self.database_url:
			return self.database_url
		return (
			f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
		)


settings = Settings()  # type: ignore