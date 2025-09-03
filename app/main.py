import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api.resumes.router import router as router_resumes
from app.api.users.router import router as router_users

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app...")
    yield
    logging.info("Stop app")


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    invalid_params = []

    for err in errors:
        loc = err.get("loc", [])
        msg = err.get("msg", "")
        # Обычно loc содержит ['body', 'parameter_name']
        if len(loc) > 1:
            param_name = loc[-1]
        else:
            param_name = loc[0] if loc else "unknown"
        invalid_params.append({param_name: msg})

    logging.error(f"validation_exception: {errors}, body: {invalid_params}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": errors,
            "invalid_params": invalid_params,
            "body": exc.body,
            "message": "validation exception",
        },
    )


app.include_router(router_resumes)

app.include_router(router_users)


origins = [
    "http://localhost:3000",
    "http://localhost:80",
    "http://176.109.106.199:80"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    logging.info(
        f"Received request: {request.method} {request.url} headers: {request.headers} body: {body}"
    )
    response = await call_next(request)
    return response


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
