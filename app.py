"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def get_home_page():
    return redirect('/users')

@app.route('/users')
def get_users_list():
    """displays a list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def add_user():
    """displays form to add a new user"""
    return render_template('add_user.html')

@app.route('/users/new', methods=['POST'])
def display_user():
    """takes form data and redirects back to user list"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pro_pic = request.form['pro_pic'] or None   # or none uses the default profile picture

    new_user = User(first_name, last_name, pro_pic)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>')
def get_user_details(user_id):
    """displays users details page"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<user_id>/edit')
def edit_user(user_id):
    """displays form to edit user information"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """takes form data and updates user information, then redirects to users list"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.pro_pic = request.form['pro_pic']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')
