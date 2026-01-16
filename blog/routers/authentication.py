from fastapi import Depends, status, APIRouter, HTTPException
from .. import schemas, models, hashing
from ..repository import blog, user
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List


from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# openssl rand -hex 32 to get a token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/login", tags=["Authentication"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


# oauth2_scheme = OAuth2PasswordBearer(token_Url="token")


def authenticate_user(request: schemas.login, db: Session = Depends(get_db)):
    user_credentials = user.get_user_email(request.username, db)
    verify_password = hashing.Hash.verify_password(
        request.password, user_credentials.password
    )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    return user_credentials


@router.post("", response_model=schemas.UserBase)
def login(request: schemas.login, db: Session = Depends(get_db)):
    return authenticate_user(request, db)
