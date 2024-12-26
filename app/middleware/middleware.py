from fastapi import Request
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from app.modules.auth.service import AuthService
from app.modules.user.repository import UserRepository
from fastapi import status
from app.core.logging import logger

class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # allow options
        if request.method == "OPTIONS":
            return Response(status_code=200)

        # allow public routes
        if request.url.path in ["/v1/api/auth/token", "/v1/public", "/v1/api/docs", "/v1/api/redoc", "/v1/openapi.json"]:
            return await call_next(request)

        #Verify token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse({"detail": "Invalid or missing token"}, status_code=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ")[1]
        try:
            auth_service = AuthService(UserRepository())
            auth_service.get_current_user(token=token)
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Expired token: {e}")
            return JSONResponse({"detail": "Expired token"}, status_code=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {e}")
            return JSONResponse({"detail": "Invalid token"}, status_code=status.HTTP_401_UNAUTHORIZED)

        return await call_next(request)