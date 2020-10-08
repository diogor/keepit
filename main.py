import uvicorn
from typing import List
from environs import Env
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from peewee import IntegrityError
from starlette.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from entities import (ContatoRequest, ContatoListResponse, ContatoResponse,
                      ContatoModel, User, UserCreateRequest, UserLoginRequest)
from services import create_contato, create_user, get_token
from middleware import BasicAuthBackend

app = FastAPI()
env = Env()
env.read_env()
database = env.str("DATABASE_URL")


origins = env.list("ORIGINS")


app.add_middleware(
    AuthenticationMiddleware, backend=BasicAuthBackend()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def lista(request: Request) -> List[ContatoListResponse]:
    contatos = ContatoModel.select().where(
            ContatoModel.user == request.user.username
        ).order_by(ContatoModel.created_at)
    return [ContatoListResponse(**c.__data__) for c in contatos]


@app.get("/{id}")
async def index(id: int) -> ContatoResponse:
    try:
        contato = ContatoModel.get(ContatoModel.id == id)
    except ContatoModel.DoesNotExist:
        raise HTTPException(status_code=404)
    return ContatoResponse(**contato.__data__)


@app.delete("/{id}")
async def delete_contato(id: int) -> JSONResponse:
    try:
        contato = ContatoModel.get(ContatoModel.id == id)
        contato.delete_instance()
    except ContatoModel.DoesNotExist:
        raise HTTPException(status_code=404)
    return JSONResponse(status_code=HTTP_202_ACCEPTED)


@app.post("/", status_code=HTTP_201_CREATED)
async def create(contato: ContatoRequest) -> ContatoResponse:
    contato = create_contato(contato)
    return contato


@app.post("/user", status_code=HTTP_201_CREATED)
async def user_create(user: UserCreateRequest) -> User:
    try:
        user = create_user(**user.dict())
    except IntegrityError:
        raise HTTPException(status_code=400)
    return User(**user.__data__)


@app.post("/token")
async def login(user: UserLoginRequest):
    return get_token(user.username, user.password)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
