
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import model_serializer
from app.config import (SessionLocal, engine, settings, pwd_settings, engine, Base, get_db)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.exceptions import AuthenticationException
from app.seeds.seeder import Seeds
from app import modules
import sys
import os
from app.modules import get_models
import importlib
from contextlib import asynccontextmanager

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def seeder():
    """This method run seeds"""
    seeder = Seeds(get_db(), modules)
    seeder.run()

def register_models():
    """
    This method register models
    """
    modules_path = "app/modules"
    module_names = [
        module
        for module in os.listdir(modules_path)
        if os.path.isdir(os.path.join(modules_path, module)) and 
           os.path.exists(os.path.join(modules_path, module, "model.py"))
    ]

    for module_name in module_names:
        import_path = f"app.modules.{module_name}.model"
        try:
            importlib.import_module(import_path)
        except Exception as e:
            print(f"Erro ao importar o módulo {import_path}: {e}")

def create_tables():
    """This method create tables"""
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on application startup."""
    create_tables()
    register_models()
    seeder()
    
    yield

app = FastAPI(
    lifespan=lifespan,
    title="FastAPI - Arquitetura MVC",
    contact={"name": "Robson Soares", "email": "robsonlimadeveloper@gmail.com"},
    # summary="FastAPI com SQLAlchemy",
    license_info={"name": "MIT License"},
    terms_of_service="https://www.example.com/terms",
    description="Exemplo de API usando FastAPI e arquitetura MVC(Model-View-Controller) e elementos de microserviços.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=True
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.openapi_schema = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

# Registre as rotas ao iniciar a aplicação
from app.core import routes

# Tratamento global de exceções
@app.exception_handler(AuthenticationException)
def authentication_exception_handler(request, exc: AuthenticationException):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "OK"}
