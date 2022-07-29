import os
from re import L
from dotenv import load_dotenv
import boto3
import uuid

from flask import Flask, jsonify, render_template, request, g

from flask_cors import CORS
# TODO:
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request

from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import ListingImage, db, connect_db, User, Message, Listing


load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
CORS(app)

# Setup the Flask-JWT-Extended extension TODO:
app.config["JWT_SECRET_KEY"] = os.environ["SECRET_KEY"]  # Change this!
jwt = JWTManager(app)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

# FIXME: Unsure if this is the right route for accessing it
SECRET_KEY = os.environ['SECRET_KEY']

######## TESTING AWS ###########################################################
s3 = boto3.resource('s3')

AWS_BUCKET = os.environ['AWS_BUCKET']


@app.get('/')
def test1():
    return render_template('index.html')


@app.post('/test')
def test():
    # TODO: can't just access one file, need all in a list
    file = request.files['test']
    # print(request.form)
    # TODO: loop over request.files to store each photo in a bucket
    #       make image url from bucket, put url in another list variable for all paths.
    #       save each in list to listing_images
    url = s3.Bucket(AWS_BUCKET).put_object(Key=file.filename, Body=file)
    return 'success'


######## LISTINGS #############################################################

@app.get('/listings')
def get_listings():
    """Gets all listings.
        Returns JSON: list of 'listing' dicts
        [ { id, owner, title, description, price_per_day, location, images: [ image , ... ] } ]
    """

    listings = Listing.query.all()

    if not listings:
        return jsonify({"listings": listings})

    serialized_listings = [listing.serialize() for listing in listings]

    return jsonify({"listings": serialized_listings})

@app.post('/listings')
@jwt_required()
def add_listing():
    """Add new listing using user id saved in g as owner_id.
        Takes { title, description, price_per_day, location, [ image_file , ... ] }

        Requires Bearer token in header.

        => If successful, returns 201 and JSON:

        { listing: {
            id, owner_id, title, description, price_per_day, location, images: [ image , ... ] }

        TODO: add schema for this
        If error, returns 400 and JSON:
        { errors, status: 400 }
    """

    # get id, form data, and files from request
    user_id = get_jwt_identity()

    files_data = request.files
    image_files = [files_data[file_name] for file_name in files_data]
    listing_data = request.form

    # create new Listing
    listing = Listing(
        owner_id=user_id,
        title=listing_data["title"],
        price_per_day=listing_data["price_per_day"],
        location=listing_data["location"],
        description=listing_data["description"]
    )
    db.session.add(listing)
    db.session.commit()

    # add each file to AWS S3 and create new ListingImage
    base_url = f'https://{AWS_BUCKET}.s3.us-west-1.amazonaws.com/'

    for file in image_files:

        image_uuid = str(uuid.uuid4())

        s3.Bucket(AWS_BUCKET).put_object(Key=(image_uuid + file.filename), Body=file)

        image_url = base_url + image_uuid + file.filename

        listing_image = ListingImage(
            listing_id=listing.id,
            path=image_url
        )

        db.session.add(listing_image)
        db.session.commit()


    return jsonify(listing=listing.serialize()), 201


@app.get('/listings/<int:listing_id>')
def get_listing(listing_id):
    """Get listing based on id in param.

        Returns JSON:
        { id, title, description, price, location, [ path, ... ] }

        if no listing with that id is found, gives a 404

    """
    listing = Listing.query.get_or_404(listing_id)
    serialized_listing = listing.serialize()

    return jsonify({"listing": serialized_listing})

#TODO:
######## MESSAGES #############################################################
@app.get('/messages')
def get_messages():
    """Gets all messages for current user using user id saved in g
        Returns JSON: list of 'messages' dicts
        [ { id, title, text, timestamp, from_user, to_user, listing_title }, ... ]
    """
    # TODO:
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
    # TODO:
    return "message returned"


@app.get('/messages/<int:message_id>')
def get_message(message_id):
    """Get message based on id in param.

        Returns JSON:
        { id, title, text, timestamp, from_user, to_user, listing_title }

    """
    # TODO:
    return "message returned"

######## USER AUTH #############################################################


@app.post('/login')
def login():
    """ Handle user login
        Takes JSON: { username, password }

        Returns JSON: { token }

        If unsuccessful, returns JSON: { "error": 'Invalid credentials' }
        with 400 status code.
    """

    user_data = request.json


    user = User.authenticate(
        user_data["username"],
        user_data["password"])

    if user:
        db.session.commit()
        #TODO: figure out expiration time
        token = create_access_token(
            identity=user.id,
            expires_delta=False)

        return jsonify(token=token)
    else:
        return jsonify({"error": 'Invalid credentials'}), 400


@app.post('/signup')
def signup():
    """ Handle user signup
        Takes JSON: { username, password, first_name, last_name }

        Returns JSON: { token }

        If unsuccessful, returns JSON: { "error": 'Invalid user profile input' }
        with 400 status code.
    """

    user_data = request.json

    try:
        user = User.signup(
            username=user_data["username"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )
        db.session.commit()
        #TODO: figure out expiration time
        token = create_access_token(
            identity=user.id,
            expires_delta=False)

        return jsonify(token=token)
    except:
        return jsonify({"error": 'Invalid user profile input'}), 400


connect_db(app)
