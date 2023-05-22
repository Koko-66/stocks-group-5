from flask import session
from flask_testing import TestCase
# import unittest

from src import create_app, db
from src.database import User

# your test cases

class UserTests(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing"
    TESTING = True 
    user=User(id=1,username='test',
                  email='test@example.com',
                  password='password')

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    # Test functions
    def test_user_crated_in_database(self):
        user=User(username='test',
                  email='test@example.com',
                  password='password')
        db.session.add(user)
        db.session.commit()

        assert user in db.session
        response = self.client.get("/") # where response from?

        # this raises an AssertionError
        assert user in db.session
    
    def test_user_log_out(self):
       pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

# if __name__ == '__main__':
#     unittest.main()