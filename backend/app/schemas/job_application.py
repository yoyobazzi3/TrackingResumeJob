from uuid import UUID
from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    saved = "saved"
    applied = "applied"
    oa = "oa"
    interview = "interview"
    rejected = "rejected"


class JobApplicationBase(BaseModel):
    company: str
    role: str
    status: ApplicationStatus = ApplicationStatus.saved
    resume_id: Optional[UUID] = None
    job_description: Optional[str] = None


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationRead(JobApplicationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class JobApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    resume_id: Optional[UUID] = None
    job_description: Optional[str] = None
