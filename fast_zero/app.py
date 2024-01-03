from fastapi import Depends, FastAPI, HTTPException, status
from pytest import Session
from sqlalchemy import select

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.security import OAuth2PasswordRequestForm
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema, Token
from fast_zero.security import get_password_hash, create_access_token, verify_password

app = FastAPI()


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"message": "Olá Mundo!"}


@app.get("/users/", status_code=status.HTTP_200_OK, response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {"users": users, "count": len(users)}


@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.username == user.username))

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
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


@app.put(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_404_NOT_FOUND,
    response_model=Message,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    session.delete(db_user)
    session.commit()

    return {"detail": "User deleted"}
