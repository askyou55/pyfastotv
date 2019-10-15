from flask_wtf import FlaskForm
from flask_babel import lazy_gettext

from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import InputRequired, Length, Email, NumberRange

from app.common.subscriber.login.entry import SubscriberUser
from app.common.subscriber.settings import Settings
import app.common.constants as constants


class SignupForm(FlaskForm):
    AVAILABLE_STATUSES = [(SubscriberUser.Status.NOT_ACTIVE, 'Not active'), (SubscriberUser.Status.ACTIVE, 'Active'),
                          (SubscriberUser.Status.TRIAL_FINISHED, 'Trial finished'),
                          (SubscriberUser.Status.BANNED, 'Banned')]

    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    password = PasswordField(lazy_gettext(u'Password:'), validators=[InputRequired(), Length(min=3, max=80)])
    country = SelectField(lazy_gettext(u'Country:'), coerce=str, validators=[InputRequired()],
                          choices=constants.AVAILABLE_COUNTRIES)
    language = SelectField(lazy_gettext(u'Language:'), coerce=str, default=constants.DEFAULT_LOCALE,
                           choices=constants.AVAILABLE_LOCALES_PAIRS)
    status = SelectField(lazy_gettext(u'Status:'), coerce=SubscriberUser.Status.coerce, validators=[InputRequired()],
                         choices=AVAILABLE_STATUSES)
    exp_date = DateTimeField(default=SubscriberUser.MAX_DATE)
    apply = SubmitField(lazy_gettext(u'Sign Up'))

    def make_entry(self) -> SubscriberUser:
        return self.update_entry(SubscriberUser())

    def update_entry(self, subscriber: SubscriberUser) -> SubscriberUser:
        subscriber.email = self.email.data
        subscriber.password = SubscriberUser.make_md5_hash_from_password(self.password.data)
        subscriber.country = self.country.data
        subscriber.language = self.language.data
        subscriber.status = self.status.data
        subscriber.exp_date = self.exp_date.data
        return subscriber


class SigninForm(FlaskForm):
    email = StringField(lazy_gettext(u'Email:'),
                        validators=[InputRequired(), Email(message=lazy_gettext(u'Invalid email')), Length(max=30)])
    password = PasswordField(lazy_gettext(u'Password:'), validators=[InputRequired(), Length(min=3, max=80)])
    submit = SubmitField(lazy_gettext(u'Sign In'))


class MessageForm(FlaskForm):
    AVAILABLE_MESSAGE_TYPES = [(constants.MessageType.TEXT, 'Text'), (constants.MessageType.HYPERLINK, 'HYPERLINK')]

    message = StringField(lazy_gettext(u'Message:'), validators=[InputRequired(), Length(max=512)])
    type = SelectField(lazy_gettext(u'Type:'), validators=[InputRequired()], choices=AVAILABLE_MESSAGE_TYPES,
                       coerce=constants.MessageType.coerce)
    ttl = IntegerField(lazy_gettext(u'Show time:'), validators=[InputRequired(), NumberRange(1, 600)])
    apply = SubmitField(lazy_gettext(u'Send'))

    def get_data(self) -> constants.PlayerMessage:
        entry = constants.PlayerMessage(self.message.data, self.ttl.data, self.type.data)
        return entry
