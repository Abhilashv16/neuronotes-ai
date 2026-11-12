
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="NeuroNotes AI",
    description="AI-powered document understanding and note generation",
    version="1.0.0"
)

# CORS for potential browser-based frontend integration.
# Native PyQt HTTP requests do not require CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def home():
    return {
        "application": "NeuroNotes AI",
        "status": "running",
        "api_version": "v1"
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "online",
        "frontend_connection": "available"
    }


@app.get("/api/v1/info")
def application_info():
    return {
        "name": "NeuroNotes AI",
        "version": "1.0.0",
        "supported_formats": ["pdf", "jpg", "jpeg", "png"],
        "database": False
    }
from api.upload import router as upload_router

app.include_router(
    upload_router,
    prefix="/api/v1",
    tags=["Document Upload"]
)

from api.documents import router as documents_router

app.include_router(
    documents_router,
    prefix="/api/v1",
    tags=["Documents"]
)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.upload import router as upload_router
from api.documents import router as documents_router
from api.processing import router as processing_router

app = FastAPI(
    title="NeuroNotes AI",
    description="AI-powered document understanding and note generation",
    version="1.0.0"
)

# CORS for possible browser-based frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
def home():
    return {
        "application": "NeuroNotes AI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "backend": "online"
    }


@app.get("/api/v1/info")
def application_info():
    return {
        "application": "NeuroNotes AI",
        "supported_formats": [".pdf", ".jpg", ".jpeg", ".png"],
        "database_enabled": False,
        "storage": "local JSON and filesystem"
    }


app.include_router(
    upload_router,
    prefix="/api/v1",
    tags=["Document Upload"]
)

app.include_router(
    documents_router,
    prefix="/api/v1",
    tags=["Document Management"]
)

app.include_router(
    processing_router,
    prefix="/api/v1",
    tags=["AI Processing"]
)
