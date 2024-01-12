from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import Todo, User


def test_create_user(session):
    new_user = User(username='Alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Alice'))

    assert user.username == 'Alice'


def test_create_todo(session: Session, user: User):
    todo = Todo(
        title='Test todo',
        description='Test todo description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
