"""SQLAlchemy models for ShareB&B."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class Message(db.Model):
    """An individual message."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(50),
        nullable=False,
    )

    text = db.Column(
        db.Text,
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    from_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    to_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )

class Listing(db.Model):
    """An individual listing."""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    title = db.Column(
        db.String(50),
        nullable=False,
    )

    price_per_day = db.Column(
        # will be python Decimal type
        db.Numeric,
        nullable=False,
    )

    location = db.Column(
        db.String(50),
        nullable=False,
    )
    #TODO: categories?

    description = db.Column(
        db.Text,
        nullable=False,
    )

    images = db.relationship(
        "ListingImage",
        backref="listing",
        passive_deletes=True
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "title": self.title,
            "price_per_day": self.price_per_day,
            "location": self.location,
            "description": self.description,
            "images": [image.serialize() for image in self.images]
        }


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    first_name = db.Column(
        db.String(40),
        nullable=False,
    )

    last_name = db.Column(
        db.String(40),
        nullable=False,
    )

    is_admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    messages_sent = db.relationship(
        "Message",
        primaryjoin=(Message.from_user_id == id)
    )

    messages_received = db.relationship(
        "Message",
        primaryjoin=(Message.to_user_id == id)
    )

    listings = db.relationship(
        "Listing",
        primaryjoin=(Listing.owner_id == id)
    )

    @classmethod
    def signup(cls, username, password, first_name, last_name):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def serialize(self):
        """Serialize user to dictionary."""

        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            # "listings": self.listings,
        }

class ListingImage(db.Model):
    """An individual image for a listing."""

    __tablename__ = 'listing_images'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )

    path = db.Column(
        db.Text,
        nullable=False
    )

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "id": self.id,
            "listing_id": self.listing_id,
            "path": self.path
        }


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

