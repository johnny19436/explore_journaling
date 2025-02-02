from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from pymongo.errors import ConnectionFailure

app = Flask(__name__)

# MongoDB Atlas connection string with database name
MONGODB_URI = "mongodb+srv://johnny194369672:qsbWWWPQiFUSeA8H@cluster0.oigb5.mongodb.net/journal_db?retryWrites=true&w=majority&appName=Cluster0"

# Use environment variable if available, otherwise use the direct connection string
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI", MONGODB_URI)

try:
    mongo = PyMongo(app)
    # Test the connection
    mongo.db.command('ping')
    print("Connected to MongoDB!")
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    raise e

# Configure CORS to allow all origins
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Serve frontend static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(f"frontend/dist/{path}"):
        return send_from_directory('frontend/dist', path)
    return send_from_directory('frontend/dist', 'index.html')

# Import routes after app is created
from app import routes

# Add error handler
@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

@app.route('/api/test')
def test():
    return jsonify({"message": "API is working"}), 200 