from mongoengine import StringField, EmbeddedDocumentField

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
    EPG_FIELD = 'epg'
    VIDEO_ENABLE_FIELD = 'video'
    AUDIO_ENABLE_FIELD = 'audio'

    def __init__(self, sid: str, epg: EpgInfo, have_video=True, have_audio=True):
        self.have_video = have_video
        self.have_audio = have_audio
        self.epg = epg
        self.id = sid

    def to_dict(self) -> dict:
        return {ChannelInfo.ID_FIELD: self.id, ChannelInfo.EPG_FIELD: self.epg.to_dict(),
                ChannelInfo.VIDEO_ENABLE_FIELD: self.have_video,
                ChannelInfo.AUDIO_ENABLE_FIELD: self.have_audio}


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
    output = EmbeddedDocumentField(OutputUrls, default=OutputUrls())  #

    def get_id(self) -> str:
        raise NotImplementedError('subclasses must override get_id()!')

    def to_channel_info(self) -> [ChannelInfo]:
        ch = []
        for out in self.output.urls:
            epg = EpgInfo(self.tvg_id, out.uri, self.name, self.tvg_logo)
            ch.append(ChannelInfo(self.get_id(), epg))
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
