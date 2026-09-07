from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_task_service
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.task import Task_service, TaskNotFound

router = APIRouter(prefix="/tasks")  


@router.get("")
def read_tasks(
    task_services: Task_service = Depends(get_task_service)
    ) -> list[Task]:
    return task_services.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    task_services: Task_service = Depends(get_task_service)
    ) -> Task:
    return task_services.create_task(task_create = payload)



@router.patch("/{task_id}", response_model=Task)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    task_services: Task_service = Depends(get_task_service)
) -> Task:
    try:
        return task_services.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: str,
    task_services: Task_service = Depends(get_task_service)
) -> None:
    try:
        return task_services.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id {task_id} not found") 