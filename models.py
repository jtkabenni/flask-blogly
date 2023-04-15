from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
default_img = "https://genslerzudansdentistry.com/wp-content/uploads/2015/11/anonymous-user.png"

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(150), nullable=True, default = default_img)

    posts = db.relationship("Post", backref="user", cascade="all, delete, delete-orphan")

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(1500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


