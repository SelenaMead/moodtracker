from enum import unique
import uuid
from datetime import datetime as dt
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login



# followers = db.Table(
#     'followers', 
#     db.Column('follower_id'))
class User(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(300))
    moodPosts = db.relationship('Post', backref='posts', cascade='all, delete-orphan')

    def generate_password(self, password_from_form):
        self.password = generate_password_hash(password_from_form)

    def check_password(self, password_from_form):
        return check_password_hash(self.password, password_from_form)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return f'<User: {self.email}>'


class Post(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    body = db.Column(db.Text)
    mood = db.Column(db.Text)
    sleep = db.Column(db.Text)
    ate = db.Column(db.Text)
    active = db.Column(db.Text)
    hygiene = db.Column(db.Text)
    meds = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=dt.utcnow)
    author = db.Column(db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'body': self.body,
            'mood': self.mood,
            'sleep': self.sleep,
            'ate': self.ate,
            'active': self.active,
            'hygiene': self.hygiene,
            'meds': self.meds,
            'date_created': self.date_created,
            'author': User.query.get(self.author)
        }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex

    def __repr__(self):
        return f'<Post: {self.body[30]}...>'


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
