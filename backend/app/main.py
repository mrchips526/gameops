from fastapi import FastAPI
from app.api.routes import router as services_router

app = FastAPI(
    title="Gameops API",
    description="Infrastructure monitoring and incident management",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "gameops-api",
        "version": "0.1.0",
    }

app.include_router(services_router, prefix="/api/v1")