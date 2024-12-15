"""Error handler."""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from core.exceptions_abstract import ErrorAbstract
from app.main import app, logger
from fastapi.exceptions import HTTPException

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    ''' Api Handle http error '''
    logger.debug(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(ErrorAbstract)
async def error_exception_handler(request: Request, exc: ErrorAbstract):
    ''' Api Handle abstract error '''
    logger.debug(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def global_handle_error(request: Request, exc: Exception):
    ''' Api Handle error '''
    logger.critical(exc.args)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc.args)}
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    ''' Api Handle validation error '''
    logger.debug(exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()}
    )
