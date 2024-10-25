from typing import List, Optional
from pydantic import BaseModel
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assignee: str
    due_data: date
    status: str
    priority: str

class TaskCreate(TaskBase):
    project_id: int

class Task(TaskBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: date
    end_date: date
    status: str

class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode = True