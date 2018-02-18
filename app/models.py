from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from app import db, bcrypt


class User(db.Model, UserMixin):

    ''' A user who has an account on the website. '''

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    confirmation = db.Column(db.Boolean)
    _password = db.Column(db.String)
    posts = db.relationship('Post', backref='users', lazy=True)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

    def __repr__(self):
        return '{}: {} - {}'.format(self.id, self.full_name, self.email)

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return '{}'.format(self.id)