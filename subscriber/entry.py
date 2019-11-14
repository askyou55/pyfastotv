from datetime import datetime
from hashlib import md5
from bson.objectid import ObjectId
from enum import IntEnum

from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, IntField, ListField, ReferenceField, \
    PULL, ObjectIdField, EmbeddedDocumentField

from app.common.service.entry import ServiceSettings
from app.common.stream.entry import IStream
import app.common.constants as constants


class Device(EmbeddedDocument):
    ID_FIELD = 'id'
    NAME_FIELD = 'name'
    STATUS_FIELD = 'status'
    CREATED_DATE_FIELD = 'created_date'

    DEFAULT_DEVICE_NAME = 'Device'
    MIN_DEVICE_NAME_LENGTH = 3
    MAX_DEVICE_NAME_LENGTH = 32

    class Status(IntEnum):
        NOT_ACTIVE = 0
        ACTIVE = 1
        BANNED = 2

        @classmethod
        def choices(cls):
            return [(choice, choice.name) for choice in cls]

        @classmethod
        def coerce(cls, item):
            return cls(int(item)) if not isinstance(item, cls) else item

        def __str__(self):
            return str(self.value)

    meta = {'allow_inheritance': False, 'auto_create_index': True}
    id = ObjectIdField(required=True, default=ObjectId, unique=True, primary_key=True)
    created_date = DateTimeField(default=datetime.now)
    status = IntField(default=Status.NOT_ACTIVE)
    name = StringField(default=DEFAULT_DEVICE_NAME, min_length=MIN_DEVICE_NAME_LENGTH,
                       max_length=MAX_DEVICE_NAME_LENGTH, required=True)

    def get_id(self):
        return str(self.id)

    def to_dict(self) -> dict:
        return {Device.ID_FIELD: self.get_id(), Device.NAME_FIELD: self.name, Device.STATUS_FIELD: self.status,
                Device.CREATED_DATE_FIELD: int(self.created_date.timestamp() * 1000)}


class Subscriber(Document):
    MAX_DATE = datetime(2100, 1, 1)
    ID_FIELD = "id"
    EMAIL_FIELD = "login"
    PASSWORD_FIELD = "password"

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

    SUBSCRIBER_HASH_LENGTH = 32

    meta = {'allow_inheritance': True, 'collection': 'subscribers', 'auto_create_index': False}

    email = StringField(max_length=64, required=True)
    password = StringField(min_length=SUBSCRIBER_HASH_LENGTH, max_length=SUBSCRIBER_HASH_LENGTH, required=True)
    created_date = DateTimeField(default=datetime.now)
    exp_date = DateTimeField(default=MAX_DATE)
    status = IntField(default=Status.NOT_ACTIVE)
    country = StringField(min_length=2, max_length=3, required=True)
    language = StringField(default=constants.DEFAULT_LOCALE, required=True)

    servers = ListField(ReferenceField(ServiceSettings, reverse_delete_rule=PULL), default=[])
    devices = ListField(EmbeddedDocumentField(Device), default=[])
    streams = ListField(ReferenceField(IStream, reverse_delete_rule=PULL), default=[])
    own_streams = ListField(ReferenceField(IStream, reverse_delete_rule=PULL), default=[])

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

    def generate_playlist(self, did: str, lb_server_host_and_port: str) -> str:
        result = '#EXTM3U\n'
        sid = str(self.id)
        for stream in self.streams:
            result += stream.generate_device_playlist(sid, self.password, did, lb_server_host_and_port, False)

        return result

    def add_official_stream(self, stream: IStream):
        self.streams.append(stream)
        self.save()

    def add_own_stream(self, stream: IStream):
        self.own_streams.append(stream)
        self.save()

    def get_not_active_devices(self):
        devices = []
        for dev in self.devices:
            if dev.status == Device.Status.NOT_ACTIVE:
                devices.append(dev.to_dict())

        return devices

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
