from fastapi import FastAPI
from app.api import health

app = FastAPI(title="AI Resume Tailor API")

app.include_router(health.router)

@app.get("/")
def root():
    return {"status": "ok"}
