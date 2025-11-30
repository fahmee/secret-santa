import hashlib
import uuid
from firebase_config import get_db
from firebase_admin import firestore

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    """Register a new user"""
    db = get_db()
    
    # Check if email already exists
    users_ref = db.collection('users')
    existing_user = users_ref.where('email', '==', email).get()
    
    if len(list(existing_user)) > 0:
        return False, "Email already registered"
    
    # Check if username already exists
    existing_username = users_ref.where('username', '==', username).get()
    if len(list(existing_username)) > 0:
        return False, "Username already taken"
    
    # Create new user
    user_id = str(uuid.uuid4())
    user_data = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'password': hash_password(password),
        'profile_completed': False,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    
    users_ref.document(user_id).set(user_data)
    return True, "Registration successful"

def login_user(email, password):
    """Authenticate user login"""
    db = get_db()
    users_ref = db.collection('users')
    
    # Find user by email
    users = users_ref.where('email', '==', email).get()
    users_list = list(users)
    
    if len(users_list) == 0:
        return False, None, "Email not found"
    
    user_doc = users_list[0]
    user_data = user_doc.to_dict()
    
    # Verify password
    if user_data['password'] == hash_password(password):
        return True, user_data, "Login successful"
    else:
        return False, None, "Incorrect password"

def get_user_by_id(user_id):
    """Get user data by user ID"""
    db = get_db()
    user_doc = db.collection('users').document(user_id).get()
    
    if user_doc.exists:
        return user_doc.to_dict()
    return None

def get_user_by_email(email):
    """Get user data by email"""
    db = get_db()
    users_ref = db.collection('users')
    users = users_ref.where('email', '==', email).get()
    users_list = list(users)
    
    if len(users_list) > 0:
        return users_list[0].to_dict()
    return None
