__author__ = 'kravets.andr@gmailcom'

from flask.ext.wtf import Form
from wtforms import validators
from wtforms.validators import Required
from wtforms.fields import TextField, BooleanField, SubmitField, PasswordField
from wtforms.widgets import HiddenInput
from manager_app.models import User


class RegistrationForm(Form):
    first_name = TextField("First name")
    last_name = TextField("Last name")
    username = TextField("Username", [Required("Please enter your username."), validators.Length(min=4)])
    password = PasswordField('Password', [Required("Please enter a password."), validators.Length(min=4)])
    is_admin = BooleanField("User is administrator")
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data.lower()).first()
        if user:
            self.username.errors.append("That username is already taken")
            return False
        else:
            return True


class UserUpdateForm(Form):
    uid = TextField("User ID", widget=HiddenInput())
    first_name = TextField("First name")
    last_name = TextField("Last name")
    username = TextField("Username", [Required("Please enter your username."), validators.Length(min=4)])
    password = PasswordField("Password")
    is_admin = BooleanField("Is user an administrator")
    update = SubmitField("Update account")
    delete = SubmitField("Delete account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        users = User.query.filter_by(username=self.username.data).all()
        if len(users) > 0 and str(users[0].uid) != str(self.uid.data):
            self.username.errors.append("That username is already taken")
            return False
        else:
            return True


class SigninForm(Form):
    username = TextField("Username", [Required("Please enter your username.")])
    password = PasswordField('Password', [Required("Please enter a password.")])
    submit = SubmitField("Sign In")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.username.errors.append("Invalid username or password")
            return False

    def is_admin(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(username=self.username.data.lower()).first()
        if user.is_administrator:
            return True
        else:
            return False