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
    
    posts = db.relationship("posts", backref="users", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about a User"""
        p = self
        return f"<User {p.id} {p.first_name} {p.last_name} {p.pro_pic}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

class Post(db.Model):
    """Posts Database Model"""
    ___tablename__ = "posts"

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
    

