from fastapi import FastAPI
from app.api import auth,users

app = FastAPI(title="AI Resume Tailor API")

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"status": "ok"}
