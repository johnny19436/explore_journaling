from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from pymongo.errors import ConnectionFailure

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')

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

@app.route('/')
def serve_frontend():
    return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
    if path.startswith('api/'):
        return app.view_functions[path]()
    return app.send_static_file(path)

# Import routes after app is created
from app import routes

# Add error handler
@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

@app.route('/api/test')
def test():
    return jsonify({"message": "API is working"}), 200 