from flask_wtf import FlaskForm
from flask_babel import lazy_gettext

from wtforms.fields import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email

from app.common.subscriber.login.entry import SubscriberUser
from app.common.subscriber.settings import Settings
import app.common.constants as constants


class SignupForm(FlaskForm):
    AVAILABLE_STATUSES = [(SubscriberUser.Status.NOT_ACTIVE, 'Not active'), (SubscriberUser.Status.ACTIVE, 'Active'),
                          (SubscriberUser.Status.TRIAL_FINISHED, 'Trial finished'),
                          (SubscriberUser.Status.BANNED, 'Banned')]

    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    password = PasswordField(lazy_gettext(u'Password:'), validators=[InputRequired(), Length(min=4, max=80)])
    country = SelectField(lazy_gettext(u'Country:'), coerce=str, validators=[InputRequired()],
                          choices=constants.AVAILABLE_COUNTRIES)
    status = SelectField(lazy_gettext(u'Status:'), coerce=SubscriberUser.Status.coerce, validators=[InputRequired()],
                         choices=AVAILABLE_STATUSES)
    apply = SubmitField(lazy_gettext(u'Sign Up'))

    def make_entry(self) -> SubscriberUser:
        return self.update_entry(SubscriberUser())

    def update_entry(self, subscriber: SubscriberUser) -> SubscriberUser:
        subscriber.email = self.email.data
        subscriber.password = SubscriberUser.make_md5_hash_from_password(self.password.data)
        subscriber.country = self.country.data
        subscriber.status = self.status.data
        return subscriber


class SigninForm(FlaskForm):
    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    password = PasswordField(lazy_gettext(u'Password:'), validators=[InputRequired(), Length(min=6, max=80)])
    submit = SubmitField(lazy_gettext(u'Sign In'))


class SettingsForm(FlaskForm):
    locale = SelectField(lazy_gettext(u'Locale:'), coerce=str, validators=[InputRequired()],
                         choices=constants.AVAILABLE_LOCALES_PAIRS)
    submit = SubmitField(lazy_gettext(u'Apply'))

    def make_settings(self) -> Settings:
        return self.update_settings(Settings())

    def update_settings(self, settings: Settings) -> Settings:
        settings.locale = self.locale.data
        return settings
