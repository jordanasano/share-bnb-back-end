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


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class BaseViewTestCase(TestCase):

    def setUp(self):
        User.query.delete()
        Listing.query.delete()
        Message.query.delete()

        # u1 has 2 listings, 1 message_sent to u2
        u1 = User.signup("u1", "password", "first1", "last1")
        # u2 has 1 listing, 1 message_sent to u1
        u2 = User.signup("u2", "password", "first2", "last2")
        u3 = User.signup("u3", "password", "first3", "last3")
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        l1 = Listing(
            owner_id=u1.id,
            title='listing1',
            price_per_day=1.00,
            location='location1',
            description='desc1'
        )
        l2 = Listing(
            owner_id=u1.id,
            title='listing2',
            price_per_day=2.00,
            location='location2',
            description='desc2'
        )
        l3 = Listing(
            owner_id=u2.id,
            title='listing3',
            price_per_day=3.00,
            location='location3',
            description='desc3'
        )
        db.session.add_all([l1, l2, l3])
        db.session.commit()

        li1 = ListingImage(
            listing_id=l1.id,
            path="https://listing_image_1.jpg"
        )

        m1 = Message(
            from_user_id=u1.id,
            to_user_id=u2.id,
            title='message1',
            text='text1',
            listing_id=l1.id
        )
        m2 = Message(
            from_user_id=u2.id,
            to_user_id=u1.id,
            title='message2',
            text='text2',
            listing_id=l1.id
        )
        db.session.add_all([m1, m2, li1])
        db.session.commit()

        #FIXME: save shit in self
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3

        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

        self.m1 = m1
        self.m2 = m2

        self.li1 = li1

        self.client = app.test_client()


    def tearDown(self):
        db.session.rollback()

class ListingsViewsTestCase(BaseViewTestCase):
    """Tests for all '/listings' routes."""

    def test_get_listings(self):
        with self.client as c:

            resp = c.get("/listings")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.l1, resp.json["listings"])
            self.assertIn(self.l2, resp.json["listings"])

    #TODO:
    # def test_add_listing(self):
    #     with self.client as c:
    #         # { title, description, price, location, [ image_file , ... ] }
    #         resp = c.post(
    #             "/listings",
    #             data={

    #             })

    #         self.assertEqual(resp.status_code, 201)
    #         self.assertIn(self.l1, resp.json["listings"])
    #         self.assertIn(self.l2, resp.json["listings"])
# class MessagesViewsTestCase(BaseViewTestCase):
#     """Tests for all '/messages' routes."""

# class AuthViewsTestCase(TestCase):
#     """Tests for user routes."""
