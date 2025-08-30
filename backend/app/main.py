from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.config import settings
from app.routers import auth as auth_router
from app.routers import rides as rides_router
from app.routers import ussd as ussd_router
from app.routers import parents as parents_router
from app.db.base import Base, engine

app = FastAPI(title=settings.app_name)

app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

logger = logging.getLogger("uvicorn.error")

@app.on_event("startup")
def on_startup():
	try:
		Base.metadata.create_all(bind=engine)
	except Exception as exc:
		logger.warning(f"DB init skipped: {exc}")

app.include_router(auth_router.router, prefix=settings.api_v1_prefix)
app.include_router(parents_router.router, prefix=settings.api_v1_prefix)
app.include_router(rides_router.router, prefix=settings.api_v1_prefix)
app.include_router(ussd_router.router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
	return {"status": "ok", "name": settings.app_name}