"""FastAPI application entrypoint and router registration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, health, resumes

app = FastAPI(title="AI Resume Tailor API")

# CORS for frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes.
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(health.router)
app.include_router(resumes.router)

@app.get("/")
def root():
    # Basic root response.
    return {"status": "ok"}
