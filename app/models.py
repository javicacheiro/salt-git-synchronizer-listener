from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    last_updated = db.Column(db.DateTime())

    def __repr__(self):
        return "<State(name='{0}', last_updated='{1}')>".format(
            self.name, self.last_updated)


class Pillar(db.Model):
    __tablename__ = 'pillars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True)
    last_updated = db.Column(db.DateTime())

    def __repr__(self):
        return "<Pillar(name='{0}', last_updated='{1}')>".format(
            self.name, self.last_updated)
