from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"


class TaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    status: Optional[TaskStatus] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    completed: Optional[bool] = None
    status: Optional[TaskStatus] = None


class TaskOut(TaskBase):
    id: int
    completed: bool
    created_at: datetime

    class Config:
        orm_mode = True
