from fastapi import FastAPI, HTTPException
from typing import Union
from pydantic import BaseModel

app = FastAPI()

todos = [
    {"id": 1, "task": "Buy groceries", "completed": False},
    {"id": 2, "task": "Finish homework", "completed": True},
    {"id": 3, "task": "Go for a run", "completed": False},
    {"id": 4, "task": "Read a book", "completed": False},
    {"id": 5, "task": "Call mom", "completed": True},
    {"id": 6, "task": "Plan a vacation", "completed": False},
    {"id": 7, "task": "Clean the house", "completed": True},
    {"id": 8, "task": "Learn Python", "completed": False},
    {"id": 9, "task": "Write a report", "completed": False},
    {"id": 10, "task": "Attend a meeting", "completed": True},
]


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Todo(BaseModel):
    task: str


@app.get('/todos')
def findAll():
    return {'data': todos}


@app.get('/todos/{id}')
def findById(id: int):
    findTodo = None
    for todo in todos:
        if (todo['id'] == id):
            findTodo = todo
            break

    if findTodo is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return {'data': todo}


@app.post('/todos')
def add(todo: Todo):
    for t in todos:
        if (t['task'] == todo.task and t['completed'] == False):
            raise HTTPException(status_code=400, detail="Item already exists")

    newTodo = {"id": todos[-1]['id']+1, "task": todo.task, "completed": False}
    todos.append(newTodo)
    return {'data': newTodo}


@app.put('/todos/{id}')
def update(id: int, todo: str):
    findTodo = None
    for todo in todos:
        if (todo['id'] == id):
            findTodo = todo
            break

    if findTodo is None:
        raise HTTPException(status_code=404, detail="Item not found")

    findTodo['task'] = todo
    return {'data': findTodo}


@app.patch('/todos/{id}/mark-complete')
def markComplete(id: int):
    for todo in todos:
        if (todo['id'] == id and todo['completed'] == False):
            todo['completed'] = True
            break
    return {'message': 'Todo marked complete'}


@app.delete('/todos/{id}')
def delete(id: int):
    findTodo = None
    for todo in todos:
        if (todo['id'] == id):
            findTodo = todo
            break

    if findTodo is None:
        raise HTTPException(status_code=404, detail="Item not found")

    todos.remove(findTodo)
    return {'message': 'Todo deleted'}
