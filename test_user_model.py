"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    # Does the repr method work as expected?
    def test_repr(self):
        """Does the repr method work as expected"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # repr should return exact format 
        self.assertEqual(u.__repr__,f'<User #{self.id}: {self.username}, {self.email}>')

    # Does is_following successfully detect when user1 is following user2?
    def test_is_following(self):
        """Does is_following succesfully detect when user1 is following user2?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        u.followers.append(u2)
        db.session.commit()

        # u2 is one of u's followers, is_following of u2 on u should return true
        self.assertTrue(u2.is_following(u))

    # Does is_following successfully detect when user1 is not following user2?
    def test_not_is_following(self):
        """Detect successfuly when a user is not following another user"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        # u2 is not following u, u2.is_following(u) should return False
        self.assertFalse(u2.is_following(u))

    # Does is_followed_by successfully detect when user1 is followed by user2?
    def test_is_followed_by(self):
        """test if is_followed_by detect successfully when a user is followed by another user"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        u.followers.append(u2)
        db.session.commit()

        # u2 is following u, therefore, u.is_followed_by(u2) should return True
        self.assertTrue(u.is_followed_by(u2))

    # Does is_followed_by successfully detect when user1 is not followed by user2?
    def test_not_is_followed_by(self):
        """test if is_followed_by detect successfully when a user is not followed by another user"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        u.followers.append(u2)
        db.session.commit()

        # u is not following u2, therefore, u2.is_followed_by(u) should return False
        self.assertFalse(u2.is_followed_by(u))

    # Does User.create successfully create a new user given valid credentials?
    def test_user_create(self):
        """Testing User.create successfully create new user given valid credentials"""
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.commit()

        # is u given valid credentials, a new user is created with a id
        # in this case, there is no other users, the id should be 1
        self.assertEqual(u.id, 1)

    # Does User.create fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?
    def test_user_create_fail(self):
        """Testing if user.create fails?"""
        u = User.signup(
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.add(u)
        try:
            db.session.commit()
        except:
            self.assertEqual(u.id, None)

    # Does User.authenticate successfully return a user when given a valid username and password?
    def test_authenticate(self);
        """Testing user.authenticate with valid credentials"""
        u = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        db.session.commit()
        u2 = User.authenticate(
            username="testuser",
            password="HASHED_PASSWORD"
        )
        
        # u2 is logged in with the registered username and password
        # u2 should have id of 1 instead of False
        self.assertEqual(u2.id, 1)
