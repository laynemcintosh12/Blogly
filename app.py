"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = True
app.config['SECRET_KEY'] = 'SEcreTT'
toolbar = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True

connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/')
def get_home_page():
    """"Render homepage with 5 most recent posts"""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', posts=posts)








# users routes -----------------------------------------------------------------------------------------------------------------------------


@app.route('/users')
def get_users_list():
    """displays a list of all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


# adding users ----------------------

@app.route('/users/new')
def add_user():
    """displays form to add a new user"""
    return render_template('add_user.html')


@app.route('/users/new', methods=['POST'])
def display_user():
    """takes form data and redirects back to user list"""
    new_user = User(first_name = request.form['first_name'],
                    last_name = request.form['last_name'],
                    pro_pic = request.form['pro_pic'] or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


# user details ------------------------


@app.route('/users/<int:user_id>')
def get_user_details(user_id):
    """displays users details page"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)


# editing a user ------------------------------


@app.route('/users/<int:user_id>/edit')
def display_edit_form(user_id):
    """displays form to edit user information"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """takes form data and updates user information, then redirects to users list"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.pro_pic = request.form['pro_pic']
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")
    return redirect('/users')


# deleting a user ---------------------------


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')












# user posts routes ---------------------------------------------------------------------------------------------------------------------------------

@app.route('/users/<int:user_id>/posts/new')
def get_post_form(user_id):
    """Shows form to add a post for a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_post(user_id):
    """handles post submission and redirects to user detail page"""
    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")
    return redirect(f"/users/{user.id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """shows the post, as well as buttons to edit or delete"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/post/<int:post_id>/edit')
def edit_post(post_id):
    """show form to edit post, as well as a cancel button"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)


@app.route('/post/<int:post_id>/edit', methods=['POST'])
def handle_edit(post_id):
    """handles the edit of a post and redirects back to post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")
    return redirect(f'/post/{post.user_id}')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes post associated with post_id"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")
    return redirect(f'/users/{post.user_id}')