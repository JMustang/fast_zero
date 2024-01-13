from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import TodoPublic, TodoSchema
from fast_zero.security import get_current_user

router = APIRouter()

CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/todos', tags=['todos'])


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=TodoPublic
)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: Session = Depends(get_session),
):
    db_todo: Todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
