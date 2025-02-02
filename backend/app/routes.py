from flask import jsonify, request
from app import app, mongo
from app.models import Journal, User
from bson import ObjectId
from functools import wraps
import jwt
import datetime

# Secret key for JWT
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split()[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = mongo.db.users.find_one({"_id": data['user_id']})
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if mongo.db.users.find_one({"email": data['email']}):
        return jsonify({"message": "Email already registered"}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    mongo.db.users.insert_one(user.to_dict())
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = mongo.db.users.find_one({"email": data['email']})
    
    if not user_data:
        return jsonify({"message": "Invalid credentials"}), 401
    
    user = User(
        username=user_data['username'],
        email=user_data['email'],
        _id=user_data['_id']
    )
    user.password_hash = user_data['password_hash']
    
    if not user.check_password(data['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = jwt.encode({
        'user_id': user._id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, app.config['SECRET_KEY'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user._id,
            'username': user.username,
            'email': user.email
        }
    })

@app.route('/api/journals', methods=['GET'])
@token_required
def get_journals(current_user):
    journals = mongo.db.journals.find()
    return jsonify([Journal(**journal).to_dict() for journal in journals])

@app.route('/api/journals', methods=['POST'])
@token_required
def create_journal(current_user):
    data = request.get_json()
    journal = Journal(
        title=data['title'],
        content=data['content'],
        author=current_user['username']
    )
    mongo.db.journals.insert_one(journal.to_dict())
    return jsonify(journal.to_dict()), 201

@app.route('/api/journals/<journal_id>', methods=['GET'])
@token_required
def get_journal(current_user, journal_id):
    journal = mongo.db.journals.find_one({"_id": journal_id})
    if journal:
        return jsonify(Journal(**journal).to_dict())
    return jsonify({"error": "Journal not found"}), 404 