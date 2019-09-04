from datetime import datetime
from hashlib import md5
from bson.objectid import ObjectId
from enum import IntEnum

from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, IntField, ListField, ReferenceField, \
    PULL, ObjectIdField, EmbeddedDocumentField

from app.common.subscriber.settings import Settings
from app.common.service.entry import ServiceSettings
from app.common.stream.entry import IStream


class Device(EmbeddedDocument):
    ID_FIELD = "id"

    DEFAULT_DEVICE_NAME = 'Device'
    MIN_DEVICE_NAME_LENGTH = 3
    MAX_DEVICE_NAME_LENGTH = 32

    meta = {'allow_inheritance': False, 'auto_create_index': True}
    id = ObjectIdField(required=True, default=ObjectId, unique=True, primary_key=True)
    created_date = DateTimeField(default=datetime.now)
    name = StringField(default=DEFAULT_DEVICE_NAME, min_length=MIN_DEVICE_NAME_LENGTH,
                       max_length=MAX_DEVICE_NAME_LENGTH,
                       required=True)


class Subscriber(Document):
    ID_FIELD = "id"
    EMAIL_FIELD = "login"
    PASSWORD_FIELD = "password"
    STATUS_FIELD = "status"
    DEVICES_FIELD = "devices"
    STREAMS_FIELD = "channels"

    class Status(IntEnum):
        NOT_ACTIVE = 0
        ACTIVE = 1
        TRIAL_FINISHED = 2
        BANNED = 3

        @classmethod
        def choices(cls):
            return [(choice, choice.name) for choice in cls]

        @classmethod
        def coerce(cls, item):
            return cls(int(item)) if not isinstance(item, cls) else item

        def __str__(self):
            return str(self.value)

    class Type(IntEnum):
        USER = 0,
        SUPPORT = 1

    SUBSCRIBER_HASH_LENGHT = 32

    meta = {'allow_inheritance': True, 'collection': 'subscribers', 'auto_create_index': False}

    email = StringField(max_length=64, required=True)
    password = StringField(min_length=SUBSCRIBER_HASH_LENGHT, max_length=SUBSCRIBER_HASH_LENGHT, required=True)
    created_date = DateTimeField(default=datetime.now)
    status = IntField(default=Status.NOT_ACTIVE)
    type = IntField(default=Type.USER)
    country = StringField(min_length=2, max_length=3, required=True)
    servers = ListField(ReferenceField(ServiceSettings, reverse_delete_rule=PULL), default=[])
    devices = ListField(EmbeddedDocumentField(Device), default=[])
    streams = ListField(ReferenceField(IStream, reverse_delete_rule=PULL), default=[])
    settings = EmbeddedDocumentField(Settings, default=Settings)

    def add_server(self, server):
        self.servers.append(server)
        self.save()

    def add_device(self, device: Device):
        self.devices.append(device)
        self.save()

    def remove_device(self, sid: str):
        for device in self.devices:
            if str(device.id) == sid:
                self.devices.remove(device)
                break
        self.save()

    def find_device(self, sid: str):
        for device in self.devices:
            if str(device.id) == sid:
                return device
        return None

    def add_stream(self, stream: IStream):
        self.streams.append(stream)
        self.save()

    def get_streams(self) -> list:
        streams = []
        for serv in self.servers:
            for stream in self.streams:
                founded_stream = serv.find_stream_settings_by_id(stream.id)
                if founded_stream:
                    channels = founded_stream.to_channel_info()
                    for ch in channels:
                        streams.append(ch.to_dict())

        return streams

    @staticmethod
    def make_md5_hash_from_password(password: str) -> str:
        m = md5()
        m.update(password.encode())
        return m.hexdigest()

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return Subscriber.make_md5_hash_from_password(password)

    @staticmethod
    def check_password_hash(hash: str, password: str) -> bool:
        return hash == Subscriber.generate_password_hash(password)


Subscriber.register_delete_rule(ServiceSettings, "subscribers", PULL)
