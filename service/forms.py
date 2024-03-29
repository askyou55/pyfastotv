from flask_wtf import FlaskForm
from flask_babel import lazy_gettext
from wtforms.fields import StringField, SubmitField, MultipleFileField, SelectField, FormField
from wtforms.validators import InputRequired, Length, Email

from app.common.common_forms import HostAndPortForm
from app.common.service.entry import ServiceSettings, ProviderPair
import app.common.constants as constants


class ServiceSettingsForm(FlaskForm):
    name = StringField(lazy_gettext(u'Name:'), validators=[InputRequired()])
    host = FormField(HostAndPortForm, lazy_gettext(u'Host:'), validators=[])
    http_host = FormField(HostAndPortForm, lazy_gettext(u'Http host:'), validators=[])
    vods_host = FormField(HostAndPortForm, lazy_gettext(u'Vods host:'), validators=[])
    cods_host = FormField(HostAndPortForm, lazy_gettext(u'Cods host:'), validators=[])

    feedback_directory = StringField(lazy_gettext(u'Feedback directory:'), validators=[InputRequired()])
    timeshifts_directory = StringField(lazy_gettext(u'Timeshifts directory:'), validators=[InputRequired()])
    hls_directory = StringField(lazy_gettext(u'Hls directory:'), validators=[InputRequired()])
    playlists_directory = StringField(lazy_gettext(u'Playlist directory:'), validators=[InputRequired()])
    dvb_directory = StringField(lazy_gettext(u'DVB directory:'), validators=[InputRequired()])
    capture_card_directory = StringField(lazy_gettext(u'Capture card directory:'), validators=[InputRequired()])
    vods_in_directory = StringField(lazy_gettext(u'Vods in directory:'), validators=[InputRequired()])
    vods_directory = StringField(lazy_gettext(u'Vods out directory:'), validators=[InputRequired()])
    cods_directory = StringField(lazy_gettext(u'Cods out directory:'), validators=[InputRequired()])
    apply = SubmitField(lazy_gettext(u'Apply'))

    def make_entry(self):
        return self.update_entry(ServiceSettings())

    def update_entry(self, settings: ServiceSettings):
        settings.name = self.name.data
        settings.host = self.host.get_data()
        settings.http_host = self.http_host.get_data()
        settings.vods_host = self.vods_host.get_data()
        settings.cods_host = self.cods_host.get_data()

        settings.feedback_directory = self.feedback_directory.data
        settings.timeshifts_directory = self.timeshifts_directory.data
        settings.hls_directory = self.hls_directory.data
        settings.playlists_directory = self.playlists_directory.data
        settings.dvb_directory = self.dvb_directory.data
        settings.capture_card_directory = self.capture_card_directory.data
        settings.vods_in_directory = self.vods_in_directory.data
        settings.vods_directory = self.vods_directory.data
        settings.cods_directory = self.cods_directory.data
        return settings


class ActivateForm(FlaskForm):
    LICENSE_KEY_LENGTH = 64

    license = StringField(lazy_gettext(u'License:'),
                          validators=[InputRequired(), Length(min=LICENSE_KEY_LENGTH, max=LICENSE_KEY_LENGTH)])
    submit = SubmitField(lazy_gettext(u'Activate'))


class UploadM3uForm(FlaskForm):
    AVAILABLE_STREAM_TYPES_FOR_UPLOAD = [(constants.StreamType.PROXY, 'Proxy Stream'),
                                         (constants.StreamType.VOD_PROXY, 'Proxy Vod'),
                                         (constants.StreamType.RELAY, 'Relay'),
                                         (constants.StreamType.ENCODE, 'Encode'),
                                         (constants.StreamType.CATCHUP, 'Catchup'),
                                         (constants.StreamType.TEST_LIFE, 'Test life'),
                                         (constants.StreamType.VOD_RELAY, 'Vod relay'),
                                         (constants.StreamType.VOD_ENCODE, 'Vod encode'),
                                         (constants.StreamType.COD_RELAY, 'Cod relay'),
                                         (constants.StreamType.COD_ENCODE, 'Cod encode'),
                                         (constants.StreamType.EVENT, 'Event')]

    files = MultipleFileField()
    type = SelectField(lazy_gettext(u'Type:'), coerce=constants.StreamType.coerce, validators=[InputRequired()],
                       choices=AVAILABLE_STREAM_TYPES_FOR_UPLOAD, default=constants.StreamType.RELAY)
    upload = SubmitField(lazy_gettext(u'Upload'))


class ServerProviderForm(FlaskForm):
    AVAILABLE_ROLES = [(ProviderPair.Roles.READ, 'Read'), (ProviderPair.Roles.WRITE, 'Write'),
                       (ProviderPair.Roles.SUPPORT, 'Support'), (ProviderPair.Roles.ADMIN, 'Admin')]

    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    role = SelectField(lazy_gettext(u'Role:'), coerce=ProviderPair.Roles.coerce, validators=[InputRequired()],
                       choices=AVAILABLE_ROLES, default=ProviderPair.Roles.ADMIN)
    apply = SubmitField(lazy_gettext(u'Apply'))
