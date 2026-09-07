from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_category_service
from app.schemas.category import Category, CategoryCreate, CategoryUpdate
from app.services.category import Category_service, CategoryNotFound

router = APIRouter(prefix="/categories")  

@router.get("")
def read_categories(
    category_services: Category_service = Depends(get_category_service)
    ) -> list[Category]:
    return category_services.list_categories()



@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    category_services: Category_service = Depends(get_category_service)
    ) -> Category:
    return category_services.create_category(category_create = payload)




@router.patch("/{category_id}", response_model=Category)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    category_services: Category_service = Depends(get_category_service)
    ) -> Category:
    return category_services.update_category(category_id=category_id, category_update=payload)



@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    category_services: Category_service = Depends(get_category_service)
    ) -> None:
    try:
        return category_services.delete_category(category_id=category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id {category_id} not found")