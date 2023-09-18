from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import (
    OAuth2PasswordRequestForm,

)
from jose import JWTError, jwt
from datetime import timedelta
import crud
import db.models as models
import db.schemas as schemas
from db.connection import SessionLocal, engine, db_dependency, get_db
from utils.jwt import get_current_active_user, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/users/signup", response_model=schemas.User)
def signup_user(user: schemas.UserCreate, db: db_dependency):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/signin", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    db_user = crud.get_user_by_email(db, email=form_data.username)
    if db_user is None or crud.match_user_password(db_user, form_data.password) is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=schemas.User)
def read_user_me(current_user: Annotated[schemas.User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/users/{user_id}/todos/", response_model=schemas.Todo)
def create_item_for_user(
    user_id: int, item: schemas.TodoCreate, db: db_dependency
):
    return crud.create_user_todo(db=db, todo=item, user_id=user_id)


@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos
