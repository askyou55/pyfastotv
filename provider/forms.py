from flask_wtf import FlaskForm
from flask_babel import lazy_gettext

from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email

import app.common.constants as constants
from app.common.provider.settings import Settings


class SettingsForm(FlaskForm):
    locale = SelectField(lazy_gettext(u'Locale:'), coerce=str, validators=[InputRequired()],
                         choices=constants.AVAILABLE_LOCALES_PAIRS)
    submit = SubmitField(lazy_gettext(u'Apply'))

    def make_settings(self):
        return self.update_settings(Settings())

    def update_settings(self, settings: Settings):
        settings.locale = self.locale.data
        return settings


class SignupForm(FlaskForm):
    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    password = PasswordField(lazy_gettext(u'Password:'), validators=[InputRequired(), Length(min=3, max=80)])
    country = SelectField(lazy_gettext(u'Country:'), coerce=str, validators=[InputRequired()],
                          choices=constants.AVAILABLE_COUNTRIES)
    submit = SubmitField(lazy_gettext(u'Sign Up'))


class SigninForm(FlaskForm):
    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    password = PasswordField(lazy_gettext(u'Password:'), validators=[InputRequired(), Length(min=3, max=80)])
    submit = SubmitField(lazy_gettext(u'Sign In'))
