import os
from dotenv import load_dotenv
import boto3

from flask import Flask, jsonify, render_template, request, g

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

######## TESTING AWS ###########################################################
s3 = boto3.resource('s3')

AWS_BUCKET = os.environ['AWS_BUCKET']
@app.get('/')
def test1():
    return render_template('index.html')

@app.post('/test')
def test():
    #TODO: can't just access one file, need all in a list
    file = request.files['test']
    # TODO: loop over request.files to store each photo in a bucket
    #       make image url from bucket, put url in another list variable for all paths.
    #       save each in list to listing_images
    url = s3.Bucket(AWS_BUCKET).put_object(Key=file.filename, Body=file)
    print('output is asduisadouiasidsao', url)
    return 'success'




@app.before_request
def get_user_id():
    """If token sent in request, get user id from token and save in g"""


######## LISTINGS #############################################################

@app.get('/listings')
def get_listings():
    """Gets all listings.
        Returns JSON: list of 'listing' dicts
        [ { id, owner, title, description, price, location, images: [ path ] } ]
    """
    #TODO:
    return "listings returned"

@app.post('/listings')
def add_listing():
    """Add new listing using user id saved in g as owner_id.

        { title, description, price, location, [ image_file , ... ] }

        => If successful, returns 201 and JSON:
        TODO: what to return to show it was added?
        { id, status: 201, title }

        If error, returns 400 and JSON:
        { errors, status: 400 }
    """
    #TODO:
    return "listing returned"


@app.get('/listings/<int:listing_id>')
def get_listing(listing_id):
    """Get listing based on id in param.

        Returns JSON:
        { id, title, description, price, location, [ path, ... ] }

    """
    #TODO:
    return "listing returned"


######## MESSAGES #############################################################
@app.get('/messages')
def get_messages():
    """Gets all messages for current user using user id saved in g
        Returns JSON: list of 'messages' dicts
        [ { id, title, text, timestamp, from_user, to_user, listing_title }, ... ]
    """
    #TODO:
    return "messages returned"

@app.post('/messages')
def add_message():
    """Add new message using user id saved in g as from_user_id.

        { title, text, listing_id }

        => If successful, returns 201 and JSON:
        TODO: what to return to show it was added?
        { id, status: 201, title }

        If error, returns 400 and JSON:
        { errors, status: 400 }
    """
    #TODO:
    return "message returned"


@app.get('/messages/<int:message_id>')
def get_message(message_id):
    """Get message based on id in param.

        Returns JSON:
        { id, title, text, timestamp, from_user, to_user, listing_title }

    """
    #TODO:
    return "message returned"

######## USER AUTH #############################################################
@app.post('/login')
def login():
    """ Handle user login TODO: takes
        Returns JSON: { token }
    """
    #TODO:
    return 'login_token'

@app.post('/signup')
def signup():
    """ Handle user signup TODO: takes
        Returns JSON: { token }
    """
    #TODO:
    return 'signup_token'


connect_db(app)