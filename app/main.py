
import sys
import os
from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from fastapi.middleware.cors import CORSMiddleware
from pydantic import model_serializer
from contextlib import asynccontextmanager
from app.config import (SessionLocal, engine, settings,
                        pwd_settings, Base, get_db)
from app import modules
from app.seeds.seeder import Seeds
from app.modules import get_models
from app.core.logging import logger
from app.middleware import middleware
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
    terms_of_service="https://www.example.com/terms",
    description="Example FastAPI application using MVC architecture and microservices elements.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    debug=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.middleware("http")
# async def log_headers(request: Request, call_next):
#     logger.info(f"Headers received: {dict(request.headers)}")
#     response = await call_next(request)
#     response_body = b"".join([chunk async for chunk in response.body_iterator])
#     logger.info(f"Response body: {response_body.decode('utf-8')}")

#     response.body_iterator = AsyncIterator(response_body)
#     return response

app.openapi_schema = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')

# Register routes
from app.core import routes, handler_error

# enable pagination
disable_installed_extensions_check()
add_pagination(app)

logger.info('API is running')
