from enum import IntEnum
import app.common.constants as constants


class EpgInfo:
    EPG_ID_FIELD = 'id'
    EPG_URLS_FIELD = 'urls'
    EPG_TITLE_FIELD = 'display_name'
    EPG_ICON_FIELD = 'icon'
    EPG_PROGRAMS_FIELD = 'programs'

    id = str
    urls = []
    title = str
    icon = str
    programs = []

    def __init__(self, eid: str, urls: [], title: str, icon: str, programs: []):
        self.id = eid
        self.urls = urls
        self.title = title
        self.icon = icon
        self.programs = programs

    def to_dict(self) -> dict:
        return {EpgInfo.EPG_ID_FIELD: self.id, EpgInfo.EPG_URLS_FIELD: self.urls, EpgInfo.EPG_TITLE_FIELD: self.title,
                EpgInfo.EPG_ICON_FIELD: self.icon, EpgInfo.EPG_PROGRAMS_FIELD: self.programs}


class BaseInfo:
    ID_FIELD = 'id'
    TYPE_FIELD = 'type'
    GROUP_FIELD = 'group'
    VIDEO_ENABLE_FIELD = 'video'
    AUDIO_ENABLE_FIELD = 'audio'

    class Type(IntEnum):
        PUBLIC = 0
        PRIVATE = 1

    def __init__(self, sid: str, ctype: Type, group: str, have_video=True, have_audio=True):
        self.id = sid
        self.type = ctype
        self.group = group
        self.have_video = have_video
        self.have_audio = have_audio

    def to_dict(self):
        return {ChannelInfo.ID_FIELD: self.id, ChannelInfo.TYPE_FIELD: self.type,
                ChannelInfo.GROUP_FIELD: self.group,
                ChannelInfo.VIDEO_ENABLE_FIELD: self.have_video,
                ChannelInfo.AUDIO_ENABLE_FIELD: self.have_audio}


class ChannelInfo(BaseInfo):
    EPG_FIELD = 'epg'

    def __init__(self, sid: str, ctype: BaseInfo.Type, group: str, epg: EpgInfo, have_video=True, have_audio=True):
        super(ChannelInfo, self).__init__(sid, ctype, group, have_video, have_audio)
        self.epg = epg

    def to_dict(self) -> dict:
        data = super(ChannelInfo, self).to_dict()
        data[ChannelInfo.EPG_FIELD] = self.epg.to_dict()
        return data


class MovieInfo:
    TITLE_FIELD = 'display_name'
    DESCRIPTION_FIELD = 'description'
    PREVIEW_ICON_FIELD = 'preview_icon'
    VOD_TYPE_FIELD = 'vod_type'
    URLS_FIELD = 'urls'

    description = str
    preview_icon = str
    vod_type = constants.VodType.VODS
    url = []

    def __init__(self, title: str, description: str, preview_icon: str, vod_type: constants.VodType, urls: []):
        self.title = title
        self.description = description
        self.preview_icon = preview_icon
        self.vod_type = vod_type
        self.urls = urls

    def to_dict(self) -> dict:
        return {MovieInfo.TITLE_FIELD: self.title, MovieInfo.DESCRIPTION_FIELD: self.description,
                MovieInfo.PREVIEW_ICON_FIELD: self.preview_icon, MovieInfo.VOD_TYPE_FIELD: self.vod_type,
                MovieInfo.URLS_FIELD: self.urls}


class VodInfo(BaseInfo):
    VOD_FIELD = 'vod'

    def __init__(self, sid: str, ctype: BaseInfo.Type, group: str, vod: MovieInfo, have_video=True, have_audio=True):
        super(VodInfo, self).__init__(sid, ctype, group, have_video, have_audio)
        self.vod = vod

    def to_dict(self) -> dict:
        data = super(VodInfo, self).to_dict()
        data[VodInfo.VOD_FIELD] = self.vod.to_dict()
        return data
