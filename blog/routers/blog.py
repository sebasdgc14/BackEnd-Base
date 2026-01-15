from fastapi import Depends, status, APIRouter
from .. import schemas
from ..repository import blog
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/blog", tags=["blog"])


# Get all blogs
@router.get("", response_model=List[schemas.Blog])
def get_all(db: Session = Depends(get_db)):
    return blog.get_all(db)


# Get specific blog
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(id, db: Session = Depends(get_db)):
    return blog.get_blog(id, db)


# Create a blog
@router.post("", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(request, db)


# Delete a blog
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, db: Session = Depends(get_db)):
    return blog.delete_blog(id, db)


# Update a blog
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(id, request, db)
