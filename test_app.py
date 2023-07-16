from unittest import TestCase
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import db, User, Post, Tag, PostTag


class TestRoutes(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Blogly2'
        return app

    def setUp(self):
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_home_page(self):
        response = self.client.get('/')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Recent Posts</h1>', html)


    def test_get_users_list(self):
        response = self.client.get('/users')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)


    def test_add_user(self):
        response = self.client.post('/users/new', data=dict(
            first_name='John',
            last_name='Doe',
            pro_pic='profile.jpg'
        ), follow_redirects=True)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)


    def test_get_user_details(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/users/{user.id}')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h3>Posts</h3>', html)


    def test_edit_user(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()

        res = self.client.post(f'/users/{user.id}/edit', data=dict(
            first_name='Updated',
            last_name='User',
            pro_pic='updated_profile.jpg'
        ), follow_redirects=True)
        html = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)


    def test_delete_user(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/users/{user.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


    def test_get_post_form(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/users/{user.id}/posts/new')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Add a New Post!</h1>', html)


    def test_handle_post(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()
        tag = Tag(name='Tag 1')
        db.session.add(tag)
        db.session.commit()

        response = self.client.post(f'/users/{user.id}/posts/new', data=dict(
            title='Test Post',
            content='This is a test post',
            tags=[tag.id]
        ), follow_redirects=True)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>John Doe</h1>', html)


    def test_handle_edit(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='This is a test post', user=user)
        db.session.add(post)
        db.session.commit()
        tag = Tag(name='Tag 1')
        db.session.add(tag)
        db.session.commit()

        response = self.client.post(f'/posts/{post.id}/edit', data=dict(
            title='Updated Post',
            content='This is an updated post',
            tags=[tag.id]
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Updated Post</h1>', html)


    def test_delete_post(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='This is a test post', user=user)
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/posts/{post.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        

    def test_get_tags_list(self):
        response = self.client.get('/tags')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Tags</h1>', html)


    def test_show_tag_detail(self):
        tag = Tag(name='Tag 1')
        db.session.add(tag)
        db.session.commit()

        response = self.client.get(f'/tags/{tag.id}')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Tag 1</h1>', html)


    def test_add_tag(self):
        response = self.client.get('/tags/new')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Create A New Tag</h1>', html)


    def test_tag_form_handler(self):
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='This is a test post', user_id='1')
        db.session.add(post)
        db.session.commit()

        response = self.client.post('/tags/new', data=dict(
            name='New Tag',
            posts=[post.id]
        ), follow_redirects=True)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Tags</h1>', html)


    def test_edit_tag(self):
        tag = Tag(name='Tag 1')
        db.session.add(tag)
        db.session.commit()

        response = self.client.get(f'/tags/{tag.id}/edit')
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Edit a tag</h1>', html)


    def test_handle_tag_edit(self):
        tag = Tag(name='Tag 1')
        db.session.add(tag)
        db.session.commit()
        user = User(first_name='John', last_name='Doe', pro_pic='profile.jpg')
        db.session.add(user)
        db.session.commit()
        post = Post(title='Test Post', content='This is a test post', user_id='1')
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/tags/{tag.id}/edit', data=dict(
            name='Updated Tag',
            posts=[post.id]
        ), follow_redirects=True)
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("<h1>Tags</h1>", html)


    def test_delete_tag(self):
        tag = Tag(name='Tag 1')
        db.session.add(tag)
        db.session.commit()

        response = self.client.post(f'/tags/{tag.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

