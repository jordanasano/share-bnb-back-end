import os
from dotenv import load_dotenv

from flask import Flask, request, g

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db


load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)



@app.before_request
def get_user_id():
    """If token sent in request, get user id from token and save in g"""


######## LISTINGS #############################################################

@app.get('/listings')
def get_listings():
    """Gets all listings.
        Returns JSON: list of 'listing' dicts
        { owner, title, description, price, location, images: [
            { path, description } ]
        }
    """
    #TODO:
    return "listings returned"

@app.post('/listings')
def add_listing():
    """Add new listing using user id saved in g as owner_id.

        { title, description, price, location, [ { image_file, description }, ... ] }

        => Returns 201 and JSON:
        TODO: what to return to show it was added?
        { id, status: 201, title }
    """
    #TODO:
    return "listing returned"


@app.get('/listings/<int:listing_id>')
def get_listing(listing_id):
    """Get listing based on id in param.

        Returns JSON:
        { title, description, price, location, [ { path, description }, ... ] }

    """
    #TODO:
    return "listing returned"

connect_db(app)