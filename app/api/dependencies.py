from fastapi import Depends

from app.services.task import Task_service
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.services.category import Category_service


def get_task_service(db: Session = Depends(get_db)) -> Task_service:
    """Функция для инъекции зависимости Task_service"""
    return Task_service(db) 

def get_category_service(db: Session = Depends(get_db)) -> Category_service:
    """Функция для инъекции зависимости Category_service"""
    return Category_service(db)