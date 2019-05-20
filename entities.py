from pydantic import BaseModel, Schema
from mongoengine import StringField, DictField, Document


class ThingModel(BaseModel):
    uid: str = None
    data: dict


class ThingDocument(Document):
    uid = StringField()
    data = DictField()