from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import Category, CategoryCreate, CategoryUpdate


class CategoryNotFound(Exception):
    """Исключение, которое возникает, когда категория не найдена в БД"""


class Category_service:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db)
    
    
    def list_categories(self) -> list[Category]:
        category_orm = self.category_repository.get_all_categories()
    
        return [Category.model_validate(category) for category in category_orm]
        
    def create_category(self, category_create: CategoryCreate) -> Category:
        category_orm = self.category_repository.create_category(name=category_create.name)
        self.db.commit()
        return Category.model_validate(category_orm)

    def update_category(self, category_id: str, category_update: CategoryUpdate) -> Category:
        category_for_update = self.category_repository.get_category_by_id(category_id)
        
        if category_update.name is not None:
            category_for_update.name = category_update.name
        self.db.commit()
        return Category.model_validate(category_for_update)

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self.category_repository.get_category_by_id(category_id)
        self.category_repository.delete_category(category_for_delete)
        self.db.commit()
        
        