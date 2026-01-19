from fastapi import Depends, status, APIRouter
from .. import schemas
from ..repository import blog
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2

router = APIRouter(prefix="/blog", tags=["blog"])


# Get all blogs
@router.get("", response_model=List[schemas.ShowBlog])
def get_all(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.get_all(db)


# Get specific blog
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog(
    id,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.get_blog(id, db)


# Create a blog
@router.post("", status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.create(request, current_user.id, db)


# Delete a blog
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
    id,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.delete_blog(id, current_user.id, db)


# Update a blog
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id,
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return blog.update_blog(id, current_user.id, request, db)
