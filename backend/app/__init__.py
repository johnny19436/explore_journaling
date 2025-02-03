from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from pymongo.errors import ConnectionFailure
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# MongoDB Atlas connection string with database name
MONGODB_URI = "mongodb+srv://johnny194369672:qsbWWWPQiFUSeA8H@cluster0.oigb5.mongodb.net/journal_db?retryWrites=true&w=majority&appName=Cluster0"

# Use environment variable if available, otherwise use the direct connection string
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI", MONGODB_URI)

try:
    mongo = PyMongo(app)
    # Test the connection
    mongo.db.command('ping')
    logger.info("Connected to MongoDB!")
except ConnectionFailure as e:
    logger.error(f"Could not connect to MongoDB: {e}")
    raise e

# Configure CORS properly
CORS(app, supports_credentials=True, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.before_request
def log_request_info():
    logger.info('Headers: %s', request.headers)
    logger.info('Body: %s', request.get_data())
    logger.info('Path: %s', request.path)
    logger.info('Method: %s', request.method)

@app.after_request
def log_response_info(response):
    logger.info('Response Status: %s', response.status)
    logger.info('Response Headers: %s', response.headers)
    return response

# Add a root route handler
@app.route('/')
def home():
    logger.info("Root route accessed")
    return jsonify({"message": "API is running"}), 200

# Import routes after app is created
from app import routes

# Add error handler
@app.errorhandler(404)
def not_found(e):
    logger.error(f"404 error: {request.url}")
    return jsonify({"error": "Route not found", "path": request.path}), 404

@app.route('/api/test')
def test():
    logger.info("Test route accessed")
    return jsonify({"message": "API is working"}), 200
 