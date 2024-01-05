from fastapi import FastAPI, status

from fast_zero.routes import auth, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=status.HTTP_200_OK)
def read_root():
    return {'message': 'Olá Mundo!'}
