# ShareBNB Backend 🏨

A Python Flask REST API backend that powers the ShareBNB web application. Hosts can list properties, guests can book them, and all users are authenticated via JWT. Integrates AWS S3 for image storage and uses PostgreSQL for persistent data.

## Features

- JWT-based authentication with `Flask-JWT-Extended`
- Role-aware endpoints for hosts and guests
- Create, update, delete, and retrieve listings
- Booking endpoints with user association
- Image upload & storage via AWS S3
- Environment management with `python-dotenv`
- CORS support for frontend integration
- Secure password storage with `Flask-Bcrypt`

## Tech Stack

- Python 3.10+
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL (via `psycopg2`)
- Boto3 (for AWS S3)
- Gunicorn (for production)
- Flask-CORS
- Python-Dotenv

## Setup Instructions

1. Clone:
   ```bash
   git clone https://github.com/jordanasano/share-bnb-back-end.git
   cd share-bnb-back-end

2. Create a virtual environment & activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
  
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Configure your environment:  
   Create a .env file in the root directory:
   ```bash
   DATABASE_URL=your_database
   SECRET_KEY=your_secret_key
   AWS_BUCKET=your_bucket_name
   ```
5. Set up your database:  
     a. If you're using raw SQL or a setup script:  
        ```bash
        psql < schema.sql
        ```
   
     b. Or, if using SQLAlchemy models:  
        ```bash
        python
        from app import db
        db.create_all()
        ```
   
7. Run the development server:
   ```bash
   flask run
   
8. For production:
   ```bash
   gunicorn app:app
   
## API Endpoints
```bash
Auth
POST /auth/signup – Register new user
POST /auth/login – Authenticate & receive JWT

Listings
GET /listings – All listings
GET /listings/<id> – Single listing
POST /listings – Create new listing (auth required)
PATCH /listings/<id> – Update listing (host only)
DELETE /listings/<id> – Delete listing (host only)

Bookings
POST /bookings – Book a stay (auth required)
GET /bookings – User's bookings

Images
POST /upload-image – Upload image to AWS S3
```

## Folder Structure
```graphql
share-bnb-back-end/
├── app.py               # Main Flask app
├── models/              # SQLAlchemy models
├── routes/              # Blueprint route handlers
├── services/            # AWS S3, auth, utilities
├── static/              # Local image fallback (optional)
├── templates/           # Email templates (optional)
├── requirements.txt
└── .env                 # Environment variables
```
