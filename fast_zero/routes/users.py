from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['Users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Session):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users, 'count': len(users)}


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def create_user(user: UserSchema, session: Session = Session):
    db_user = session.scalar(
        select(User).where(User.username == user.username)
    )

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already exists',
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_password,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.put(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not enough permissions',
        )

    current_user.username = user.username
    current_user.password = user.password
    current_user.email = user.email
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_404_NOT_FOUND,
    response_model=Message,
)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions',
        )

    # db_user = session.scalar(select(User).where(User.id == user_id))

    # if db_user is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #     )

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}
