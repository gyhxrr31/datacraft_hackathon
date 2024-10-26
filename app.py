from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Project, Task
from schemas import Project, ProjectCreate, Task, TaskCreate
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
import crud

# Инициализация базы данных
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Клиентский порт
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Создание проекта
@app.post('/api/project/', response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db=db, project=project)

# Чтение всех проектов
@app.get('/api/projects/', response_model=list[Project])
def read_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db=db)

# Чтение проекта по ID
@app.get('/api/projects/{project_id}', response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail='Проект не найден')
    return db_project

# Создание задачи
@app.post('/api/tasks/', response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

# Генерация отчета по проектам и задачам
@app.get("/api/report/", response_model=dict)
def generate_report(db: Session = Depends(get_db)):
    projects = crud.get_projects(db)

    # Проверка, если проекты не найдены
    if not projects:
        raise HTTPException(status_code=404, detail="Проекты не найдены")

    # Подготовка данных для визуализации
    labels = []
    values = []
    
    for project in projects:
        labels.append(project.name)
        tasks = crud.get_tasks_by_project_id(db=db, project_id=project.id)

        # Проверка наличия задач для каждого проекта
        if not tasks:
            values.append(0)  # Если задач нет, добавляем 0 в значение
            continue

        completed_tasks = sum(task.is_completed for task in tasks)
        total_tasks = len(tasks)
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        values.append(completion_rate)

    # Формирование ответа с данными для графика
    return {
        "title": "Отчет по выполнению задач по проектам",
        "labels": labels,
        "values": values
    }
