from typing import List
from datetime import datetime
from uuid import uuid4
from mongoengine import connect
from environs import Env
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from entities import ThingModel, ThingDocument

app = FastAPI()
env = Env()
env.read_env()
database = env.str("DATABASE_URL")
connect(host=database)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_thing(thing: ThingModel) -> ThingModel:
    if not thing.tag:
        thing.tag = format(int(datetime.now().timestamp()), 'x') + uuid4().hex
    thing_doc = ThingDocument(tag=thing.tag, data=thing.data)
    thing_doc.save()
    return thing


@app.get("/{key}")
async def index(key: str) -> List[ThingDocument]:
    things = ThingDocument.objects.filter(tag=key)
    return [thing.data for thing in things]


@app.post("/", status_code=HTTP_201_CREATED)
async def create(thing: ThingModel) -> ThingModel:
    thing = create_thing(thing)
    return thing
