from flask import jsonify, request
from app import app, mongo
from app.models import Journal, User
from bson import ObjectId
from functools import wraps
import jwt
import datetime
import os

# Secret key for JWT
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-for-development')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            print("No token found")
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # Remove 'Bearer ' prefix if it exists
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            print(f"Decoding token: {token}")
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(f"Token data: {data}")
            
            current_user = mongo.db.users.find_one({"_id": data['user_id']})
            if not current_user:
                print("User not found")
                return jsonify({'message': 'User not found'}), 401
                
            print(f"User authenticated: {current_user['username']}")
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {str(e)}")
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return jsonify({'message': 'Authentication failed'}), 401
    return decorated

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
            
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400
        
        # Check if email exists
        existing_user = mongo.db.users.find_one({"email": data['email']})
        if existing_user:
            return jsonify({"message": "Email already registered"}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        
        result = mongo.db.users.insert_one(user.to_dict())
        if result.inserted_id:
            return jsonify({"message": "User created successfully"}), 201
        return jsonify({"message": "Failed to create user"}), 500
            
    except Exception as e:
        print(f"Error in signup: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

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
    try:
        print(f"Getting journals for user: {current_user['username']}")
        journals = list(mongo.db.journals.find())
        return jsonify([Journal(**journal).to_dict() for journal in journals])
    except Exception as e:
        print(f"Error getting journals: {str(e)}")
        return jsonify({'message': 'Error retrieving journals'}), 500

@app.route('/api/journals', methods=['POST'])
@token_required
def create_journal(current_user):
    try:
        print("Received journal creation request")
        data = request.get_json()
        print(f"Request data: {data}")
        
        if not data:
            return jsonify({"message": "No data provided"}), 400
            
        if 'title' not in data or 'content' not in data:
            return jsonify({"message": "Missing required fields"}), 400

        journal = Journal(
            title=data['title'],
            content=data['content'],
            author=current_user['username']
        )
        print(f"Created journal object: {journal.to_dict()}")
        
        result = mongo.db.journals.insert_one(journal.to_dict())
        print(f"Insert result: {result.inserted_id}")
        
        if result.inserted_id:
            return jsonify(journal.to_dict()), 201
        return jsonify({"message": "Failed to create journal"}), 500
    except Exception as e:
        print(f"Error creating journal: {str(e)}")
        return jsonify({"message": str(e)}), 400

@app.route('/api/journals/<journal_id>', methods=['GET'])
@token_required
def get_journal(current_user, journal_id):
    journal = mongo.db.journals.find_one({"_id": journal_id})
    if journal:
        return jsonify(Journal(**journal).to_dict())
    return jsonify({"error": "Journal not found"}), 404 