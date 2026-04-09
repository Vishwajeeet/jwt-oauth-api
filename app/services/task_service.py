from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.exceptions import TaskNotFoundException, UnauthorizedAccessException

class TaskService:
    @staticmethod
    def create_task(task_create: TaskCreate, user: User, db: Session) -> Task:
        """Create a new task for a user."""
        task = Task(
            title=task_create.title,
            description=task_create.description,
            owner_id=user.id
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def get_user_tasks(user: User, db: Session) -> List[Task]:
        """Get all tasks for a user."""
        return db.query(Task).filter(Task.owner_id == user.id).all()
    
    @staticmethod
    def get_task_by_id(task_id: uuid.UUID, user: User, db: Session) -> Task:
        """Get a specific task by ID."""
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            raise TaskNotFoundException()
        
        if task.owner_id != user.id and not user.is_admin:
            raise UnauthorizedAccessException()
        
        return task
    
    @staticmethod
    def update_task(
        task_id: uuid.UUID,
        task_update: TaskUpdate,
        user: User,
        db: Session
    ) -> Task:
        """Update a task."""
        task = TaskService.get_task_by_id(task_id, user, db)
        
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def delete_task(task_id: uuid.UUID, user: User, db: Session) -> None:
        """Delete a task."""
        task = TaskService.get_task_by_id(task_id, user, db)
        db.delete(task)
        db.commit()
