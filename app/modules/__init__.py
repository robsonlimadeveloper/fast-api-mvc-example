# pylint: disable=import-error
"""Init module"""
import os
import sys
from typing import List, Any, Dict
from dotenv import load_dotenv, find_dotenv
import importlib
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Any

load_dotenv(find_dotenv())

def get_named_modules() -> List[str]:
    """Get module name"""
    modules: List[str] = os.listdir(f'{sys.path[0]}{os.environ["MODULE_PATH"]}')
    directories: List[str] = []

    for module in modules:
        if not module in ('__init__.py', '__pycache__'):
            directories.append(module)

    return directories

def get_models() -> Dict[str, DeclarativeMeta]:
    """Get module classes inheriting from Base."""
    module_path = "app/modules/"
    module_dir = os.path.join(sys.path[0], module_path)
    modules = os.listdir(module_dir)
    models = {}

    for module in modules:
        if module not in ("__init__.py", "__pycache__"):
            try:
                import_path = f"{module_path.replace('/', '.')}{module}"
                imported_module = importlib.import_module(import_path)
                
                for attr_name in dir(imported_module):
                    attr = getattr(imported_module, attr_name)
                    if isinstance(attr, DeclarativeMeta):
                        models[attr_name] = attr
            except Exception as e:
                print(f"Erro ao carregar o módulo {module}: {e}")

    return models


__all__ = get_named_modules() # type: ignore