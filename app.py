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

############# LISTINGS #########################################################
@app.get('/listings')
def get_listings():
    """ Takes no input. 
        Returns:
            [
                {
                    owner, 
                    title, 
                    description, 
                    price, 
                    location, 
                    images: [{path, description}, ...]
                }, 
                ...
            ]
    """

connect_db(app)