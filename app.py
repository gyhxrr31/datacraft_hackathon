from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Project, Task
from schemas import Project, ProjectCreate, Task, TaskCreate
from fastapi.middleware.cors import CORSMiddleware


import crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/projects/', response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

@app.get('/projects/', response_model=list[Project])
def read_projects(db: Session = Depends(get_db)):
    return crud.get_project(db=db)


@app.get('projects/{project_id}', response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code404, detail='Проект не найден')
    return db_project

@app.post('/tasks/', response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешите запросы с клиентского порта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
