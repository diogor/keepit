import os
import hashlib
from base64 import b64encode
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


class User(BaseModel):
    id: int
    name: str
    username: str


class Token(BaseModel):
    token: str


class ContatoModel(BaseDBModel):
    retorno = peewee.CharField()
    texto = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.now)


class UserModel(BaseDBModel):
    name = peewee.CharField()
    username = peewee.CharField(unique=True)
    password = peewee.CharField()
    salt = peewee.CharField(default=b64encode(os.urandom(32)).decode('utf-8'))
    token = peewee.CharField(null=True)
    created_at = peewee.DateTimeField(default=datetime.now)

    def set_password(self, password: str) -> None:
        self.password = b64encode(
            hashlib.pbkdf2_hmac('sha256',
                                password.encode(),
                                self.salt.encode(),
                                100000)).decode('utf-8')

    def check_password(self, password: str) -> bool:
        key = b64encode(hashlib.pbkdf2_hmac(
                        'sha256', password.encode(),
                        self.salt.encode(), 100000)).decode('utf-8')
        return self.password == key


def create_tables():
    db.connect()
    db.create_tables([ContatoModel, UserModel])


if __name__ == '__main__':
    create_tables()
