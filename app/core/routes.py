"""Routes base."""
import importlib
import sys
import os
from fastapi import APIRouter
from app.main import app
from app.core.logging import logger

def include_router_from_module(target, module):
    module_attributes = vars(module)
    
    for attribute in module_attributes.values():
        if isinstance(attribute, APIRouter):
            target.include_router(attribute)

def register_routes():
    """Register routes from modules."""
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
                logger.error(f"Failed to import {module}: {e}")

# Register routes
register_routes()

# Routes base
@app.get("/api/v1", tags=["API Index"])
def api_index():
    """API index base."""
    routes = []
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            routes.append({"path": route.path, "methods": list(route.methods)})
    return {"routes": routes}
