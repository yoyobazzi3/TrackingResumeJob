# app/schemas/resume.py

from pydantic import BaseModel
from uuid import UUID
from typing import Dict, Any


class ResumeCreateRequest(BaseModel):
    content: Dict[str, Any]


class ResumeResponse(BaseModel):
    id: UUID
    content: Dict[str, Any]
    is_frozen: bool

    class Config:
        from_attributes = True


class ResumeListResponse(BaseModel):
    id: UUID
    is_frozen: bool

    class Config:
        from_attributes = True
