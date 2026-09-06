from fastapi import Depends

from app.services.task import Task_service
from app.db.session import get_db
from sqlalchemy.orm import Session


def get_task_service(db: Session = Depends(get_db)) -> Task_service:
    """Функция для инъекции зависимости Task_service"""
    return Task_service(db) 