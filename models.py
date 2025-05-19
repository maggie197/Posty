from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    galleries = db.relationship('Gallery', back_populates='user', cascade='all, delete')

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # correct place
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', back_populates='galleries')
    photos = db.relationship('Photo', back_populates='gallery', cascade='all, delete')

# ... rest of your classes unchanged ...

class Photo(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    filename    = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery_id  = db.Column(db.Integer, db.ForeignKey('gallery.id'), nullable=False)

    gallery   = db.relationship('Gallery', back_populates='photos')
    comments  = db.relationship('Comment', back_populates='photo', cascade='all, delete')

class Comment(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    text      = db.Column(db.Text, nullable=False)
    created   = db.Column(db.DateTime, default=datetime.utcnow)
    photo_id  = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    photo = db.relationship('Photo', back_populates='comments')
    user  = db.relationship('User')

