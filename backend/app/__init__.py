from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongodb:27017/journal_db"
mongo = PyMongo(app)
CORS(app)

from app import routes 