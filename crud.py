from sqlalchemy.orm import Session
from schemas import ProjectCreate, TaskCreate
from models import Project, Task


# Получить проект по идентификатору
def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


# Получить список всех проектов
def get_projects(db: Session):
    return db.query(Project).all()


# Создать новый проект
def create_project(db: Session, project: ProjectCreate):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# Создать новую задачу для проекта
def create_task(db: Session, task: TaskCreate):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


# Получить задачи для определенного проекта
def get_tasks_by_project_id(db: Session, project_id: int):
    return db.query(Task).filter(Task.project_id == project_id).all()


# Генерация отчета по проекту, включая все задачи
def generate_report(db: Session, project_id: int):
    project = get_project(db, project_id)
    if not project:
        return None  # Проект не найден

    tasks = get_tasks_by_project_id(db, project_id)
    
    # Структура отчета
    report_data = {
        "project_id": project.id,
        "project_name": project.name,
        "description": project.description,
        "tasks": [
            {
                "task_id": task.id,
                "task_name": task.name,
                "task_status": task.status,
                "due_date": task.due_date
            } for task in tasks
        ]
    }
    return report_data
