import os
from unittest import TestCase
from models import User, Message, Listing, ListingImage, db

# Use test database
os.environ['DATABASE_URL'] = "postgresql:///share_bnb_test"

from app import app

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class BaseViewTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        Listing.query.delete()
        Message.query.delete()

        # u1 = User.signup("u1", "password", "first1", "last1")
        # u2 = User.signup("u2", "password", "first2", "last2")
        # u3 = User.signup("u3", "password", "first3", "last3")
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()

        # self.u1_id = u1.id
        # self.u2_id = u2.id
        # self.u3_id = u3.id

        u1 = User.signup("u1", "password", "first1", "last1")
        u2 = User.signup("u2", "password", "first2", "last2")
        u3 = User.signup("u3", "password", "first3", "last3")
        db.session.add_all([u1, u2, u3])
        db.session.commit()
        l1 = Listing(
                    owner_id=u1.id,
                    title='listing',
                    price_per_day=1.50,
                    location='sf',
                    description='in the bay'
                )
        l2 = Listing(
                    owner_id=u2.id,
                    title='listing',
                    price_per_day=1.50,
                    location='sf',
                    description='in the bay'
                )
        db.session.add_all([l1,l2])
        db.session.commit()
        m1 = Message(
                    from_user_id=u1.id,
                    to_user_id=u2.id,
                    title='sf',
                    text='test message',
                    listing_id=l1.id
                )
        m2 = Message(
            from_user_id=u1.id,
            to_user_id=u2.id,
            title='sf',
            text='test message',
            listing_id=l1.id
        )
        db.session.add_all([m1,m2])
        db.session.commit()
        
        self.client = app.test_client()

    def test(self):
        self.assertIn('asdasd')
    # def tearDown(self):
    #     db.session.rollback()

# class ListingsViewsTestCase(BaseViewTestCase):
#     """Tests for all '/listings' routes."""

# class MessagesViewsTestCase(BaseViewTestCase):
#     """Tests for all '/messages' routes."""

# class AuthViewsTestCase(TestCase):
#     """Tests for user routes."""