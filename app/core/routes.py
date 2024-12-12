import importlib
import traceback
from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from app import app
from app.modules import get_named_modules  # Supondo que essa função retorna os módulos necessários

# Inicialize o objeto APIRouter, que será usado para registrar as rotas
router = APIRouter()

def register_routes():
    for named_module in get_named_modules():  # Assume que retorna uma lista de módulos (ex: ['user', 'auth'])
        try:
            # Tente importar o módulo de visualizações das rotas do módulo
            module = importlib.import_module(f'app.modules.{named_module}.views')
            # Assuma que o módulo tem um objeto 'router' que define as rotas
            router.include_router(getattr(module, 'router'))
        except ModuleNotFoundError as e:
            print(f'Módulo não encontrado: {e}')
        except Exception as e:
            print(f'Erro ao importar o módulo {named_module}: {traceback.format_exc()}')

# Registre as rotas ao iniciar a aplicação
register_routes()

# Endpoint base da API
@app.get("/api")
def index():
    """api index base"""
    link_serializable = []
    for route in app.routes:
        link_serializable.append(str(f"{route.path} {route.methods}"))
    return JSONResponse(content={"Rotas": link_serializable})
