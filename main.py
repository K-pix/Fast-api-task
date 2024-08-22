from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import date

app = FastAPI()

# Enum for Task Status
class StatusEnum(str, Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

# Pydantic model for a Task
class Task(BaseModel):
    title: str
    date: date
    description: Optional[str] = None
    project: Optional[str] = None
    status: StatusEnum = StatusEnum.TODO

# In-memory "database"
tasks_db = []

@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

@app.get("/tasks/", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.put("/tasks/{task_index}", response_model=Task)
def update_task(task_index: int, task: Task):
    if task_index < 0 or task_index >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db[task_index] = task
    return task

@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}
