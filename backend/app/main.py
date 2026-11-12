from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .database import connect, initialize
from .routers import cocktails
from .schemas import Health


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield


app = FastAPI(title="SipWise API", version="0.1.0", lifespan=lifespan)
app.include_router(cocktails.router, prefix="/api/v1")


@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    code = {
        404: "NOT_FOUND",
        422: "VALIDATION_ERROR",
    }.get(exc.status_code, "REQUEST_ERROR")
    return JSONResponse(
        {"error": {"code": code, "message": str(exc.detail)}},
        status_code=exc.status_code,
        headers=exc.headers,
    )


@app.exception_handler(RequestValidationError)
async def validation_error(request: Request, exc: RequestValidationError):
    return JSONResponse(
        {"error": {"code": "VALIDATION_ERROR", "message": "Check the request fields"}},
        status_code=422,
    )


@app.get("/api/v1/health", tags=["health"])
def health() -> Health:
    with connect() as connection:
        connection.execute("SELECT 1 FROM cocktails LIMIT 1").fetchone()
    return Health()
