from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session, mapped_column

from app.models.base import Base
from app.db.session import engine

from app.api.routers.task import router as task_router








    

    
class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str]
    
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan = lifespan)
app.include_router(router=task_router, prefix="/api/v1")
#app.include_router(router=category_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


    




    

    



        

def category_orm_to_model(category_orm: CategoryORM) -> Category:
    return Category(id=category_orm.id, name=category_orm.name)



@app.get("/categories")
def read_categories(db:Session = Depends(get_db)) -> list[Category]:
    category_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in category_from_db]



@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db:Session = Depends(get_db)) -> Category:
    new_category = CategoryORM(name=payload.name)
    db.add(new_category)
    db.commit()

    return category_orm_to_model(new_category)




@app.patch("/categories/{category_id}", response_model=Category)
def update_category(category_id: str, payload: CategoryCreate, db:Session = Depends(get_db)) -> Category:
    category_for_update = db.get(CategoryORM, category_id)
    if not category_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_for_update.name = payload.name
    db.commit()
    return category_orm_to_model(category_for_update)



@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db:Session = Depends(get_db) ) -> None:
    category_for_delete = db.get(CategoryORM, category_id)
    db.delete(category_for_delete)
    db.commit()