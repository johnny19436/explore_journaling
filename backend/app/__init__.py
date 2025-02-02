from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI", "mongodb://mongodb:27017/journal_db")
mongo = PyMongo(app)
CORS(app)

# Add a root route handler
@app.route('/')
def home():
    return "API is running"

# Import routes after app is created
from app import routes

# Add error handler
@app.errorhandler(404)
def not_found(e):
    return {"error": "Route not found"}, 404

@app.route('/api/test')
def test():
    return jsonify({"message": "API is working"}), 200 