from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.utils.rate_limiter import limiter
from app.routers import auth, oauth, users, tasks
from app.config import settings

app = FastAPI(
    title="JWT OAuth API",
    description="Production-grade REST API with JWT + OAuth2 + RBAC",
    version="1.0.0"
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "JWT OAuth API is running"
    }

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "JWT OAuth API",
        "version": "1.0.0",
        "description": "Production-grade REST API with JWT + OAuth2 + RBAC",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }