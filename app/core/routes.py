from ast import mod
import importlib
import traceback
import sys
import os
from fastapi import APIRouter, FastAPI
from app.modules import get_named_modules  # Supondo que essa função retorna os módulos necessários
from app.main import app

def include_router_from_module(target, module):
    module_attributes = vars(module)
    
    for attribute in module_attributes.values():
        if isinstance(attribute, APIRouter):
            target.include_router(attribute)

def register_routes():
    """Registra rotas a partir dos arquivos `views.py` em cada módulo."""
    module_path = "app/modules/"
    module_dir = os.path.join(sys.path[0], module_path)
    modules = os.listdir(module_dir)

    for module in modules:
        if module not in ("__init__.py", "__pycache__"):
            try:
                import_path = f"{module_path.replace('/', '.')}{module}.views"
                imported_module = importlib.import_module(import_path)
                include_router_from_module(app, imported_module)
            except Exception as e:
                print(f"Erro ao carregar o módulo {module}: {e}")

# Registra as rotas ao iniciar a aplicação
register_routes()

# Endpoint base da API
@app.get("/api", tags=["API Index"])
def api_index():
    """API index base."""
    routes = []
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            routes.append({"path": route.path, "methods": list(route.methods)})
    return {"routes": routes}
