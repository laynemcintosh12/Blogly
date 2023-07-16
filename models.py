"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users Database Models"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    first_name = db.Column(db.Text,
                        nullable=False)
    last_name = db.Column(db.Text,
                        nullable=False)
    pro_pic = db.Column(db.Text, 
                        default='https://i.stack.imgur.com/l60Hf.png')
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about a User"""
        p = self
        return f"<User {p.id} {p.first_name} {p.last_name} {p.pro_pic}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    """Posts Database Model"""
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(15),
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    
    @property
    def friendly_date(self):
        """Return date time."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    

class PostTag(db.Model):
    """Connects Post model to Tags model"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
    

class Tag(db.Model):
    """Tags data model"""
    __tablename__ = "tags"

    id = db.Column(db.Integer, 
                   primary_key=True)
    name = db.Column(db.Text, 
                     nullable=False, 
                     unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        cascade="all,delete",
        backref="tags",
    )