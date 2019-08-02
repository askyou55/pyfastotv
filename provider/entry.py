from mongoengine import Document, StringField, DateTimeField, IntField, EmbeddedDocumentField, ListField, \
    ReferenceField, PULL
from datetime import datetime
from enum import IntEnum
from werkzeug.security import generate_password_hash, check_password_hash

from app.common.provider.settings import Settings
from app.common.service.entry import ServiceSettings


class Provider(Document):
    class Status(IntEnum):
        NO_ACTIVE = 0
        ACTIVE = 1
        BANNED = 2

    class Type(IntEnum):
        GUEST = 0,
        USER = 1

    meta = {'allow_inheritance': True, 'collection': 'providers', 'auto_create_index': False}
    email = StringField(max_length=30, required=True)
    password = StringField(required=True)
    created_date = DateTimeField(default=datetime.now)
    status = IntField(default=Status.NO_ACTIVE)
    type = IntField(default=Type.USER)
    country = StringField(min_length=2, max_length=3, required=True)

    settings = EmbeddedDocumentField(Settings, default=Settings)
    servers = ListField(ReferenceField(ServiceSettings, reverse_delete_rule=PULL), default=[])

    def add_server(self, server):
        self.servers.append(server)
        self.save()

    def remove_server(self, server):
        self.servers.remove(server)
        self.save()

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return generate_password_hash(password, method='sha256')

    @staticmethod
    def check_password_hash(hash: str, password: str) -> bool:
        return check_password_hash(hash, password)
