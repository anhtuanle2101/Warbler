"""User View Test"""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py

import os
import TestCase from unittest

from models import db, connect_db, User, Message

os.environ['DATABASE_URL'] = 'postgresql:///warbler-test'

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """User View Tests"""

    def setUp(self):

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.test_user = User.signup(
            username="testuser",
            email="test@test.com",
            password="testuser",
            image_url=None
        )

        db.session.commit()

    def test_log_in(self):
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.test_user.id
            
            res = c.post('/login', data={'username':'testuser', 'password':'testuser'}, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(self.test_user.username, html)

    def test_log_out(self):
        with self.client as c:
            with c.session_transaction() as s:
                s[CURR_USER_KEY] = self.test_user.id

            res = c.get('/logout', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(self.test_user.username, html)
            self.assertIn('Log in', html)

            
