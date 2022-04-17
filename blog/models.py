from datetime import datetime
from blog import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(15), unique=True, nullable= False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable= False)
    picture = db.Column(db.String(20), nullable=False, default='cat.jpg')
    posts = db.relationship('Posts', backref="author", lazy= True)

    def get_token(self, expires_sec= 1800):
        token = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return token.dumps({'user_id': self.id }).decode('utf-8')

    @staticmethod
    def verify_token(token):
        t = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = t.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"(username: {self.username}, email:{self.email}, picture:{self.picture})"

class Posts(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String, nullable= False)
    content = db.Column(db.Text, nullable= False)
    time = db.Column(db.DateTime, default= datetime.utcnow, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)

    def __repr__(self):
        return f"(title:{self.title},time:{self.time})"
