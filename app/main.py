from fastapi import FastAPI

app = FastAPI(
    title="JWT OAuth API",
    description="Production-grade REST API with JWT + OAuth2 + RBAC",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "JWT OAuth API is running"
    }