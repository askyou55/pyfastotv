from mongoengine import EmbeddedDocument, StringField
import app.common.constants as constants


class Settings(EmbeddedDocument):
    locale = StringField(default=constants.DEFAULT_LOCALE)
