import uvicorn
from typing import List
from environs import Env
from fastapi import FastAPI, Request
from peewee import IntegrityError
from starlette.status import (HTTP_201_CREATED, HTTP_404_NOT_FOUND,
                              HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from entities import (ContatoRequest, ContatoResponse,
                      ContatoModel, User, UserCreateRequest)
from services import create_contato, create_user

app = FastAPI()
env = Env()
env.read_env()
database = env.str("DATABASE_URL")


origins = env.list("ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def lista() -> List[ContatoResponse]:
    contatos = ContatoModel.select().order_by(ContatoModel.created_at)
    return [ContatoResponse(**c.__data__) for c in contatos]


@app.get("/{id}")
async def index(id: int) -> ContatoResponse:
    try:
        contato = ContatoModel.get(ContatoModel.id == id)
    except ContatoModel.DoesNotExist:
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={'message': 'Not Found.'}
        )
    return ContatoResponse(**contato.__data__)


@app.post("/", status_code=HTTP_201_CREATED)
async def create(contato: ContatoRequest) -> ContatoResponse:
    contato = create_contato(contato)
    return contato


@app.post("/user", status_code=HTTP_201_CREATED)
async def user_create(user: UserCreateRequest) -> User:
    try:
        user = create_user(**user.dict())
    except IntegrityError:
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={'message': 'Username exists.'}
        )
    return User(**user.__data__)


@app.middleware("http")
async def check_token(request: Request, call_next):
    method = request.scope.get('method')
    path = request.scope.get('path')
    response = await call_next(request)
    if method == 'POST' and path == '/':
        return response
    auth = request.headers.get('authorization')
    if auth:
        token = auth.split('Token')[1]
        return response
    return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={'message': 'Unauthorized.'}
            )
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
