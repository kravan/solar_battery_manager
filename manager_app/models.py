__author__ = 'kravets.andr@gmailcom'

from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(54))
    is_admin = db.Column(db.Boolean(False))

    def __init__(self, first_name, last_name, username, password, is_admin=False):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.username = username.lower()
        self.set_password(password)
        self.is_admin = is_admin

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
