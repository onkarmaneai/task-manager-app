from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.database.models import Task, User
from app.schemas.task import TaskCreate, TaskStatus, TaskUpdate


def _resolve_completed(status: TaskStatus | None, completed: bool | None) -> bool | None:
    if status is None:
        return completed
    return status == TaskStatus.completed


def create_task(db: Session, user: User, payload: TaskCreate) -> Task:
    completed = _resolve_completed(payload.status, None) or False
    task = Task(
        title=payload.title,
        description=payload.description,
        completed=completed,
        user_id=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, user: User) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.user_id == user.id)
        .order_by(Task.created_at.desc())
        .all()
    )


def get_task(db: Session, user: User, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
    if not task:
        raise NotFoundError(code="TASK_NOT_FOUND", message="Task not found.")
    return task


def update_task(db: Session, user: User, task_id: int, payload: TaskUpdate) -> Task:
    task = get_task(db, user, task_id)
    update_data = payload.dict(exclude_unset=True)
    status = update_data.pop("status", None)
    completed = _resolve_completed(status, update_data.pop("completed", None))
    for field, value in update_data.items():
        setattr(task, field, value)
    if completed is not None:
        task.completed = completed
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, user: User, task_id: int) -> None:
    task = get_task(db, user, task_id)
    db.delete(task)
    db.commit()
