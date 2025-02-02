from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password=None, _id=None):
        self._id = _id if _id else str(ObjectId())
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password) if password else None
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash
        }

class Journal:
    def __init__(self, title, content, author, created_at=None, _id=None):
        self._id = _id if _id else str(ObjectId())
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at if created_at else datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "title": self.title,
            "content": self.content,
            "author": self.author,
            "created_at": self.created_at
        } 