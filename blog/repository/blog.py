from fastapi import Depends, status, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session


# Returns all blogs
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


# Get specific blog
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return blog


# Create a blog
def create(request: schemas.Blog, current_user_id, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, body=request.body, user_id=current_user_id
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Delete a blog
def delete_blog(id, current_user_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        if blog.user_id == current_user_id:
            db.query(models.Blog).filter(models.Blog.id == id).delete(
                synchronize_session=False
            )
            db.commit()
            return "Deleted succesfully"
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this blog",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog can't be deleted because it doesnt exist",
        )


# Update a blog
def update_blog(
    id: int, current_user_id: int, request: schemas.Blog, db: Session = Depends(get_db)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog:
        if blog.user_id == current_user_id:
            db.query(models.Blog).filter(models.Blog.id == id).update(
                request.model_dump(), synchronize_session=False
            )
            db.commit()
            return "Updated succesfully"
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this blog",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog can't be updated because it doesnt exist",
        )
