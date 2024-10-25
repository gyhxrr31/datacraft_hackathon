from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)

    tasks = relationship('Task', back_populates='project', cascade='all, delete-orphan')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    title = Column(String(150), nullable=False)
    desription = Column(Text, nullable=True)
    assingee = Column(String(50), nullable=False)
    due_data = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=False)

    project = relationship('Project', back_populates='tasks')
