from flask_wtf import FlaskForm

from flask_babel import lazy_gettext
from wtforms.fields import StringField, SubmitField
from wtforms.validators import InputRequired, Length

from app.common.epg.entry import Epg

import app.common.constants as constants


class EpgForm(FlaskForm):
    uri = StringField(lazy_gettext(u'Url:'),
                      validators=[InputRequired(),
                                  Length(min=constants.MIN_URL_LENGTH, max=constants.MAX_URL_LENGTH)])
    apply = SubmitField(lazy_gettext(u'Apply'))

    def make_entry(self) -> Epg:
        return self.update_entry(Epg())

    def update_entry(self, entry: Epg) -> Epg:
        entry.uri = self.uri.data
        return entry
