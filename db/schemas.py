from pydantic import BaseModel, Field, EmailStr


class TodoBase(BaseModel):
    task: str = Field(..., min_length=1, max_length=50)
    completed: bool = False  # default value of completed is False


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    owner_id: int


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    # todos: list[Todo] = []

    class Config:
        from_attributes = True
