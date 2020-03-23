from mongoengine import connect
from environs import Env
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED
from starlette.middleware.cors import CORSMiddleware
from entities import Contato, ContatoModel

app = FastAPI()
env = Env()
env.read_env()
database = env.str("DATABASE_URL")
connect(host=database)


origins = env.list("ORIGINS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_contato(contato: Contato) -> Contato:
    contato_doc = ContatoModel(retorno=contato.retorno, texto=contato.texto)
    contato_doc.save()
    return contato


@app.get("/{id}")
async def index(id: int) -> ContatoModel:
    contato = ContatoModel.get(ContatoModel.id == id)
    return contato


@app.post("/", status_code=HTTP_201_CREATED)
async def create(contato: Contato) -> Contato:
    contato = create_contato(contato)
    return contato
