from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.config import settings

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
	if creds is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
	try:
		payload = jwt.decode(creds.credentials, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
		user_id = int(payload.get("sub"))
		return user_id
	except (JWTError, ValueError):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")