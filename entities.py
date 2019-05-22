from pydantic import BaseModel, Schema
from mongoengine import StringField, DictField, Document


class ThingModel(BaseModel):
    tag: str = None
    data: dict


class ThingDocument(Document):
    tag = StringField()
    data = DictField()