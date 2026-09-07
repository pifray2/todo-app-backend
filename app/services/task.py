from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import Task, TaskCreate, TaskUpdate


class TaskNotFound(Exception):
    """Исключение, которое возникает, когда задача не найдена в БД"""


class Task_service:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)
        
    def list_tasks(self) -> list[Task]:
        tasks_orm = self.task_repository.get_all_tasks()
    
        return [Task.model_validate(task) for task in tasks_orm]
        
    def create_task(self, task_create: TaskCreate) -> Task:
        task_orm = self.task_repository.create_task(title=task_create.title)
        self.db.commit()
        return Task.model_validate(task_orm)
        
        
    def update_task(self, task_id: str, task_update: TaskUpdate) -> Task:
        task_for_update = self.task_repository.get_task_by_id(task_id)
        
        if task_update.title is not None:
            task_for_update.title = task_update.title 
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        
        self.db.commit()
        return Task.model_validate(task_for_update)
        
    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repository.get_task_by_id(task_id)
        self.task_repository.delete_task(task_for_delete)
        self.db.commit()