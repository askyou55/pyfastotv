from enum import IntEnum

import app.common.constants as constants


class EpgInfo:
    EPG_ID_FIELD = 'id'
    EPG_URLS_FIELD = 'urls'
    EPG_TITLE_FIELD = 'display_name'
    EPG_ICON_FIELD = 'icon'
    EPG_PROGRAMS_FIELD = 'programs'

    id = str
    url = str
    title = str
    icon = str
    programs = []

    def __init__(self, eid: str, urls: [], title: str, icon: str, programs=list()):
        self.id = eid
        self.urls = urls
        self.title = title
        self.icon = icon
        self.programs = programs

    def to_dict(self) -> dict:
        return {EpgInfo.EPG_ID_FIELD: self.id, EpgInfo.EPG_URLS_FIELD: self.urls, EpgInfo.EPG_TITLE_FIELD: self.title,
                EpgInfo.EPG_ICON_FIELD: self.icon, EpgInfo.EPG_PROGRAMS_FIELD: self.programs}


class ChannelInfo:
    ID_FIELD = 'id'
    TYPE_FIELD = 'type'
    STREAM_TYPE_FIELD = 'stream_type'
    GROUP_FIELD = 'group'
    DESCRIPTION_FIELD = 'description'
    PREVIEW_ICON_FIELD = 'preview_icon'
    EPG_FIELD = 'epg'
    VIDEO_ENABLE_FIELD = 'video'
    AUDIO_ENABLE_FIELD = 'audio'

    class Type(IntEnum):
        PUBLIC = 0
        PRIVATE = 1

    def __init__(self, sid: str, ctype: Type, stream_type: constants.StreamType, group: str, description: str,
                 preview_icon: str, epg: EpgInfo,
                 have_video=True,
                 have_audio=True):
        self.have_video = have_video
        self.have_audio = have_audio
        self.epg = epg
        self.id = sid
        self.type = ctype
        self.stream_type = stream_type
        self.group = group
        self.description = description
        self.preview_icon = preview_icon

    def to_dict(self) -> dict:
        return {ChannelInfo.ID_FIELD: self.id, ChannelInfo.TYPE_FIELD: self.type,
                ChannelInfo.STREAM_TYPE_FIELD: self.stream_type,
                ChannelInfo.GROUP_FIELD: self.group,
                ChannelInfo.DESCRIPTION_FIELD: self.description,
                ChannelInfo.PREVIEW_ICON_FIELD: self.preview_icon,
                ChannelInfo.EPG_FIELD: self.epg.to_dict(),
                ChannelInfo.VIDEO_ENABLE_FIELD: self.have_video,
                ChannelInfo.AUDIO_ENABLE_FIELD: self.have_audio}
