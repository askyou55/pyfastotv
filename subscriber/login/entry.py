from flask_login import UserMixin, login_user, logout_user

from app.common.subscriber.entry import Subscriber


def login_user_wrap(user):
    login_user(user)


class SubscriberUser(UserMixin, Subscriber):
    def logout(self):
        logout_user()

    @classmethod
    def make_subscriber(cls, email: str, password: str, country: str, language: str):
        return cls(email=email, password=Subscriber.make_md5_hash_from_password(password), country=country,
                   language=language)
