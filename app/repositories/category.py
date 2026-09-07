



from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def get_all_categories(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()
    
    def get_category_by_id(self, category_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)
    
    def create_category(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete_category(self, category: CategoryORM) -> None:
        self.db.delete(category)
        self.db.commit()