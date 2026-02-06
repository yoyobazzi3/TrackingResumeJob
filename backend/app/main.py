"""FastAPI application entrypoint and router registration."""

from fastapi import FastAPI
from app.api import auth,users

app = FastAPI(title="AI Resume Tailor API")

# Register API routes.
app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    # Basic root response.
    return {"status": "ok"}
