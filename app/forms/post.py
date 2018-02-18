from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import (Required, Length, Email, ValidationError,
                                EqualTo)
from app.models import User, Post


class Create(Form):

    title = TextField(
        validators=[Required(), Length(min=5)],
        description='Title'
    )
    body = TextField(
        validators=[],
        description='Body'
    )