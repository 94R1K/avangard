from flask_bcrypt import Bcrypt

from . import db

bcrypt = Bcrypt()


class DataModel(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.String(255))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'<Пользователь {self.username}>'

    def check_password(self, password):
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        return bcrypt.check_password_hash(pw_hash, password)
