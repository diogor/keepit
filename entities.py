from pydantic import BaseModel
from datetime import datetime
from playhouse.db_url import connect
from environs import Env
import peewee


env = Env()
env.read_env()
database = env.str("DATABASE_URL")
db = connect(database)


class BaseDBModel(peewee.Model):
    class Meta:
        database = db


class ContatoResponse(BaseModel):
    id: int
    retorno: str
    created_at: datetime


class ContatoRequest(BaseModel):
    retorno: str
    texto: str


class ContatoModel(BaseDBModel):
    retorno = peewee.CharField()
    texto = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.now)


def create_tables():
    db.connect()
    db.create_tables([ContatoModel])


if __name__ == '__main__':
    create_tables()
