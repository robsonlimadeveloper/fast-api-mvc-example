
import sys
import os
from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import (SessionLocal, engine, settings,
                        pwd_settings, Base, get_db)
from app import modules
from app.seeds.seeder import Seeds
from app.core.logging import logger
from app.middleware.middleware import JWTMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.core.utils import AsyncIterator

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

logger.info('API is starting up')

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on application startup."""
    
    seeder = Seeds(get_db(), modules)
    seeder.create_tables()
    seeder.register_models()
    seeder.run()
    seeder.synchronize_sequences()

    yield

app = FastAPI(
    lifespan=lifespan,
    title="FastAPI - MVC Architecture",
    contact={"name": "Robson Soares",
             "email": "robsonlimadeveloper@gmail.com"},
    # summary="FastAPI",
    license_info={"name": "MIT License"},
    # terms_of_service="https://www.example.com/terms",
    description="Example FastAPI application using MVC architecture and microservices elements.",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/api/docs",
    redoc_url="/v1/api/redoc",
    debug=True
)


app.add_middleware(JWTMiddleware)

# origins = [
#     "http://localhost:4010",
#     "http://127.0.0.1:4010",
#     "https://meudominio.com",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log headers

# @app.middleware("http")
# async def log_headers(request: Request, call_next):
#     logger.info(f"Headers received: {dict(request.headers)}")
#     response = await call_next(request)
#     response_body = b"".join([chunk async for chunk in response.body_iterator])
#     logger.info(f"Response body: {response_body.decode('utf-8')}")

#     response.body_iterator = AsyncIterator(response_body)
#     return response

app.openapi_schema = None
security = OAuth2PasswordBearer("/v1/api/auth/token")

# Register routes
from app.core import routes, handler_error

# enable pagination
disable_installed_extensions_check()
add_pagination(app)

logger.info('API is running')

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    # session_cookie="my_session",
    # max_age=3600,  # Expira após 1 hora
)