"""Seed file to make sample data for blogly db."""

from models import User, Post, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()
Tag.query.delete()

# Add users
whiskey = User(first_name='Whiskey',
                last_name="dog")
bowser = User(first_name='Bowser', 
              last_name="cat")
spike = User(first_name='Spike', 
             last_name="porcupine")

# Add tags
tag1 = Tag(name='funny')
tag2 = Tag(name='sad')
tag3 = Tag(name='mean')


# Add posts
post1 = Post(title="first post",
             content="hello I am whiskey",
             user_id=1)
post2 = Post(title="second post",
             content="hello I am bowser",
             user_id=2)
post3 = Post(title="third post",
             content="hello I am spike",
             user_id=3)





# Add new objects to session and commit
db.session.add_all([whiskey,bowser,spike,tag1,tag2,tag3,post1,post2,post3])
db.session.commit()