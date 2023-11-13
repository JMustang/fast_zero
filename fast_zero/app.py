from fastapi import FastAPI, HTTPException, status

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/users/', status_code=status.HTTP_200_OK, response_model=UserList)
def read_users():
    return {'users': database}


@app.post(
    '/users/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)
    return user_with_id


@app.put(
    '/users/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=status.HTTP_404_NOT_FOUND,
    response_model=Message,
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del database[user_id - 1]

    return {'detail': 'User deleted'}
