# from fastapi import Request
# from app.core.logging import logger
# from app.main import app

# @app.middleware("http")
# async def log_headers(request: Request, call_next):
#     logger.info(f"Headers recebidos: {dict(request.headers)}")
#     response = await call_next(request)
#     logger.info(f"Headers de resposta: {dict(response.headers)}")
#     return response