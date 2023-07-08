"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Users Database Models"""
    __tablename__ = "Users"

    id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    first_name = db.Column(db.String(15),
                        nullable=False)
    last_name = db.Column(db.String(20),
                        nullable=False)
    pro_pic = db.Column(db.Text, 
                        nullable=True, 
                        default='https://i.stack.imgur.com/l60Hf.png')

    def __repr__(self):
        """Show info about a User"""
        p = self
        return f"<User {p.id} {p.first_name} {p.last_name} {p.pro_pic}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)