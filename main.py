from typing import List
from environs import Env
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
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
    user = create_user(user)
    return user
