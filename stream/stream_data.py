from enum import IntEnum
from mongoengine import StringField, EmbeddedDocumentField, ListField, FloatField

from app.common.common_entries import OutputUrls

import app.common.constants as constants


class EpgInfo:
    EPG_ID_FIELD = 'id'
    EPG_URL_FIELD = 'url'
    EPG_TITLE_FIELD = 'display_name'
    EPG_ICON_FIELD = 'icon'
    EPG_PROGRAMS_FIELD = 'programs'

    id = str
    url = str
    title = str
    icon = str
    programs = []

    def __init__(self, eid: str, url: str, title: str, icon: str, programs=list()):
        self.id = eid
        self.url = url
        self.title = title
        self.icon = icon
        self.programs = programs

    def to_dict(self) -> dict:
        return {EpgInfo.EPG_ID_FIELD: self.id, EpgInfo.EPG_URL_FIELD: self.url, EpgInfo.EPG_TITLE_FIELD: self.title,
                EpgInfo.EPG_ICON_FIELD: self.icon, EpgInfo.EPG_PROGRAMS_FIELD: self.programs}


class ChannelInfo:
    ID_FIELD = 'id'
    TYPE_FIELD = 'type'
    STREAM_TYPE_FIELD = 'stream_type'
    GROUP_FIELD = 'group'
    TAGS_FIELD = 'tags'
    EPG_FIELD = 'epg'
    VIDEO_ENABLE_FIELD = 'video'
    AUDIO_ENABLE_FIELD = 'audio'

    class Type(IntEnum):
        PUBLIC = 0
        PRIVATE = 1

    def __init__(self, sid: str, ctype: Type, stream_type: constants.StreamType, group: str, tags: list, epg: EpgInfo,
                 have_video=True,
                 have_audio=True):
        self.have_video = have_video
        self.have_audio = have_audio
        self.epg = epg
        self.id = sid
        self.type = ctype
        self.stream_type = stream_type
        self.group = group
        self.tags = tags

    def to_dict(self) -> dict:
        return {ChannelInfo.ID_FIELD: self.id, ChannelInfo.TYPE_FIELD: self.type,
                ChannelInfo.STREAM_TYPE_FIELD: self.stream_type,
                ChannelInfo.GROUP_FIELD: self.group,
                ChannelInfo.TAGS_FIELD: self.tags,
                ChannelInfo.EPG_FIELD: self.epg.to_dict(),
                ChannelInfo.VIDEO_ENABLE_FIELD: self.have_video,
                ChannelInfo.AUDIO_ENABLE_FIELD: self.have_audio}


class StreamDataFields:  # UI field
    NAME = 'name'
    ID = 'id'
    ICON = 'icon'
    PRICE = 'price'
    GROUP = 'group'
    TAGS = 'tags'


class IStreamData(object):
    tvg_id = StringField(default=constants.DEFAULT_STREAM_TVG_ID, max_length=constants.MAX_STREAM_TVG_ID_LENGTH,
                         min_length=constants.MIN_STREAM_TVG_ID_LENGTH,
                         required=True)
    name = StringField(default=constants.DEFAULT_STREAM_NAME, max_length=constants.MAX_STREAM_NAME_LENGTH,
                       min_length=constants.MIN_STREAM_NAME_LENGTH, required=True)
    tvg_name = StringField(default=constants.DEFAULT_STREAM_TVG_NAME, max_length=constants.MAX_STREAM_NAME_LENGTH,
                           min_length=constants.MIN_STREAM_NAME_LENGTH, required=True)  #
    tvg_logo = StringField(default=constants.DEFAULT_STREAM_ICON_URL, max_length=constants.MAX_URL_LENGTH,
                           min_length=constants.MIN_URL_LENGTH, required=True)  #
    group_title = StringField(default=constants.DEFAULT_STREAM_GROUP_TITLE,
                              max_length=constants.MAX_STREAM_GROUP_TITLE_LENGTH,
                              min_length=constants.MIN_STREAM_GROUP_TITLE_LENGTH, required=True)
    tags = ListField(StringField(max_length=constants.MAX_STREAM_GROUP_TITLE_LENGTH,
                                 min_length=constants.MIN_STREAM_GROUP_TITLE_LENGTH), default=[])

    price = FloatField(default=0.0, min_value=constants.MIN_PRICE, max_value=constants.MAX_PRICE, required=True)

    output = EmbeddedDocumentField(OutputUrls, default=OutputUrls())  #

    def get_id(self) -> str:
        raise NotImplementedError('subclasses must override get_id()!')

    def to_channel_info(self, ctype: ChannelInfo.Type, utype: constants.StreamType) -> [ChannelInfo]:
        ch = []
        for out in self.output.urls:
            epg = EpgInfo(self.tvg_id, out.uri, self.name, self.tvg_logo)
            ch.append(ChannelInfo(self.get_id(), ctype, utype, self.group_title, self.tags, epg))
        return ch

    def generate_playlist(self, header=True) -> str:
        result = '#EXTM3U\n' if header else ''
        for out in self.output.urls:
            result += '#EXTINF:-1 tvg-id="{0}" tvg-name="{1}" tvg-logo="{2}" group-title="{3}",{4}\n{5}\n'.format(
                self.tvg_id,
                self.tvg_name,
                self.tvg_logo,
                self.group_title,
                self.name,
                out.uri)

        return result

    def to_dict(self) -> dict:
        return {StreamDataFields.NAME: self.name, StreamDataFields.ID: self.get_id(),
                StreamDataFields.ICON: self.tvg_logo, StreamDataFields.PRICE: self.price,
                StreamDataFields.GROUP: self.group_title, StreamDataFields.TAGS: self.tags}
