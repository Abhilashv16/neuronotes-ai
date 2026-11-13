
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from api.upload import router as upload_router
from api.documents import router as documents_router
from api.processing import router as processing_router

app = FastAPI(
    title="NeuroNotes AI",
    description="AI-powered document understanding and note generation",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Register API routers
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
        "backend": "online",
        "frontend_connection": "available"
    }


@app.get("/api/v1/info")
def application_info():
    return {
        "application": "NeuroNotes AI",
        "supported_formats": [
            ".pdf", ".jpg", ".jpeg", ".png"
        ],
        "database_enabled": False,
        "storage": "local JSON and filesystem"
    }
    
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    for model in schema.get("components", {}).get("schemas", {}).values():
        for prop in model.get("properties", {}).values():

            # Fix single-file fields
            if prop.get("contentMediaType") == "application/octet-stream":
                prop.pop("contentMediaType")
                prop["format"] = "binary"

            # Fix multiple-file fields
            items = prop.get("items", {})
            if items.get("contentMediaType") == "application/octet-stream":
                items.pop("contentMediaType")
                items["format"] = "binary"

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi