from firebase_config import get_db
from firebase_admin import firestore
import random

def save_user_profile(user_id, shipping_address, wishlist, anti_wishlist):
    """Save user profile details"""
    db = get_db()
    
    profile_data = {
        'user_id': user_id,
        'shipping_address': shipping_address,
        'wishlist': wishlist,
        'anti_wishlist': anti_wishlist,
        'updated_at': firestore.SERVER_TIMESTAMP
    }
    
    # Update user profile
    db.collection('profiles').document(user_id).set(profile_data)
    
    # Mark profile as completed in users collection
    db.collection('users').document(user_id).update({
        'profile_completed': True
    })
    
    return True

def get_user_profile(user_id):
    """Get user profile details"""
    db = get_db()
    profile_doc = db.collection('profiles').document(user_id).get()
    
    if profile_doc.exists:
        return profile_doc.to_dict()
    return None

def get_all_users():
    """Get all registered users"""
    db = get_db()
    users_ref = db.collection('users')
    users = users_ref.stream()
    
    return [user.to_dict() for user in users]

def create_secret_santa_assignments(admin_user_id):
    """Create Secret Santa assignments for all users"""
    db = get_db()
    
    # Get all users
    users = get_all_users()
    user_ids = [user['user_id'] for user in users]
    
    if len(user_ids) < 2:
        return False, "Need at least 2 users to create assignments"
    
    # Create a derangement (no one gets themselves)
    receivers = user_ids.copy()
    random.shuffle(receivers)
    
    # Ensure no one gets themselves
    attempts = 0
    max_attempts = 100
    while attempts < max_attempts:
        valid = True
        for i, giver in enumerate(user_ids):
            if giver == receivers[i]:
                valid = False
                break
        
        if valid:
            break
        
        random.shuffle(receivers)
        attempts += 1
    
    if attempts >= max_attempts:
        return False, "Could not generate valid assignments"
    
    # Save assignments
    assignments_ref = db.collection('assignments')
    
    # Clear existing assignments
    existing = assignments_ref.stream()
    for doc in existing:
        doc.reference.delete()
    
    # Create new assignments
    for giver, receiver in zip(user_ids, receivers):
        assignment_data = {
            'giver_id': giver,
            'receiver_id': receiver,
            'revealed': False,
            'created_at': firestore.SERVER_TIMESTAMP
        }
        assignments_ref.add(assignment_data)
    
    return True, "Assignments created successfully"

def get_user_assignment(user_id):
    """Get the Secret Santa assignment for a user"""
    db = get_db()
    assignments_ref = db.collection('assignments')
    
    # Find assignment where this user is the giver
    assignments = assignments_ref.where('giver_id', '==', user_id).get()
    assignments_list = list(assignments)
    
    if len(assignments_list) > 0:
        return assignments_list[0].to_dict()
    return None

def mark_assignment_revealed(user_id):
    """Mark that a user has revealed their assignment"""
    db = get_db()
    assignments_ref = db.collection('assignments')
    
    assignments = assignments_ref.where('giver_id', '==', user_id).get()
    for assignment in assignments:
        assignment.reference.update({'revealed': True})

def get_random_question():
    """Get a random question from the questions collection"""
    db = get_db()
    questions_ref = db.collection('questions')
    
    # Get all questions
    questions = list(questions_ref.stream())
    
    if len(questions) == 0:
        # Initialize default questions if none exist
        initialize_default_questions()
        questions = list(questions_ref.stream())
    
    # Select a random question
    question_doc = random.choice(questions)
    question_data = question_doc.to_dict()
    
    # Randomize answer options
    options = question_data['options'].copy()
    random.shuffle(options)
    
    question_data['options'] = options
    return question_data

def initialize_default_questions():
    """Initialize default questions in the database"""
    db = get_db()
    questions_ref = db.collection('questions')
    
    default_questions = [
        {
            'question': 'What is Santa\'s favorite color?',
            'options': ['Red', 'Green', 'Blue', 'Yellow'],
            'correct_answer': 'Red'
        },
        {
            'question': 'How many reindeer does Santa have?',
            'options': ['6', '8', '9', '10'],
            'correct_answer': '9'
        },
        {
            'question': 'What do people traditionally put on top of a Christmas tree?',
            'options': ['Star', 'Angel', 'Snowflake', 'Bell'],
            'correct_answer': 'Star'
        },
        {
            'question': 'In which country did the tradition of putting up a Christmas tree originate?',
            'options': ['USA', 'England', 'Germany', 'France'],
            'correct_answer': 'Germany'
        },
        {
            'question': 'What is the name of the Grinch\'s dog?',
            'options': ['Max', 'Rex', 'Buddy', 'Charlie'],
            'correct_answer': 'Max'
        },
        {
            'question': 'What are Christmas songs called?',
            'options': ['Hymns', 'Carols', 'Ballads', 'Anthems'],
            'correct_answer': 'Carols'
        },
        {
            'question': 'What do naughty kids get for Christmas?',
            'options': ['Nothing', 'Coal', 'Sticks', 'Rocks'],
            'correct_answer': 'Coal'
        },
        {
            'question': 'What is Rudolph\'s special feature?',
            'options': ['Red Nose', 'White Tail', 'Golden Antlers', 'Blue Eyes'],
            'correct_answer': 'Red Nose'
        }
    ]
    
    for question in default_questions:
        questions_ref.add(question)

def get_username_by_id(user_id):
    """Get username by user ID"""
    db = get_db()
    user_doc = db.collection('users').document(user_id).get()
    
    if user_doc.exists:
        return user_doc.to_dict().get('username')
    return None

def get_all_usernames_except(exclude_user_id):
    """Get all usernames except the specified user ID"""
    db = get_db()
    users = get_all_users()
    
    usernames = []
    for user in users:
        if user['user_id'] != exclude_user_id:
            usernames.append(user['username'])
    
    return usernames
