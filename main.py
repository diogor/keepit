from datetime import datetime
from uuid import uuid4
from mongoengine import connect
from environs import Env
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from starlette.responses import JSONResponse
from entities import ThingModel, ThingDocument

app = FastAPI()
env = Env()
env.read_env()
database = env.str("DATABASE_URL")
connect(database)


def create_thing(thing: ThingModel):
    thing.uid = format(int(datetime.now().timestamp()), 'x') + uuid4().hex
    thing_doc = ThingDocument(uid=thing.uid, data=thing.data)
    thing_doc.save()
    return thing


@app.get("/{key}")
async def index(key: str):
    try:
        thing = ThingDocument.objects.get(uid=key)
    except ThingDocument.DoesNotExist:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND)
    return thing.data


@app.post("/", status_code=HTTP_201_CREATED)
async def create(thing: ThingModel):
    thing = create_thing(thing)
    return thing
