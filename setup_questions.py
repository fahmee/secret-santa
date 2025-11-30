"""
Script to add quiz questions to Firebase database
Run this to populate the questions collection
"""

from firebase_config import get_db
from firebase_admin import firestore

def add_questions_to_db():
    """Add quiz questions to Firebase"""
    db = get_db()
    questions_ref = db.collection('questions')
    
    # Clear existing questions (optional)
    print("Clearing existing questions...")
    existing = questions_ref.stream()
    for doc in existing:
        doc.reference.delete()
    print("✓ Existing questions cleared")
    
    # Add your custom questions here
    questions = [
        {
            'question': 'I come with many colours, so beautiful and bright; I turn so many houses into a beautiful sight. What am I?',
            'options': ['Christmas lights', 'A cold', 'A candle', 'Fire'],
            'correct_answer': 'Christmas lights'
        },
        {
            'question': 'You can catch me easily, especially around Christmas, but you can\'t throw me. What am I?',
            'options': ['Christmas lights', 'A cold', 'A candle', 'Fire'],
            'correct_answer': 'A cold'
        },
        {
            'question': 'I\'m tall when I\'m young and short when I\'m old. Though you light me up every Christmas, I\'m not the cold. What am I?',
            'options': ['Christmas lights', 'A cold', 'A candle', 'Fire'],
            'correct_answer': 'A candle'
        },
        {
            'question': 'I\'m not alive, but I can grow; I don\'t have lungs, but I need air; I don\'t have a mouth, but water kills me. During Christmas, I bring warmth and light. What am I?',
            'options': ['Christmas lights', 'A cold', 'A candle', 'Fire'],
            'correct_answer': 'Fire'
        },
        {
            'question': 'I get chopped, decorated, and on one end you\'ll see wings. I\'m not a turkey and I\'m not an angel, but I am a central figure in your Christmas scene. What am I?',
            'options': ['A Christmas tree', 'A candy cane', 'Snow', 'Christmas lights'],
            'correct_answer': 'A Christmas tree'
        },
        {
            'question': 'In your Christmas stocking, you might find me. I\'m not a toy, but I\'m hard to eat without getting messy. I\'m striped and sweet, but I\'m not a shoe. What am I?',
            'options': ['A Christmas tree', 'A candy cane', 'Snow', 'Christmas lights'],
            'correct_answer': 'A candy cane'
        },
        {
            'question': 'I drop from up high, but never get hurt. I\'m often white, but I\'m not a shirt. What am I?',
            'options': ['A Christmas tree', 'A candy cane', 'Snow', 'Fire'],
            'correct_answer': 'Snow'
        }
    ]
    
    # Add questions to database
    print("\nAdding questions to database...")
    for idx, question in enumerate(questions, 1):
        questions_ref.add(question)
        print(f"✓ Added question {idx}: {question['question']}")
    
    print(f"\n🎉 Successfully added {len(questions)} questions to the database!")
    print("\nYou can now use the app and answer these questions to reveal Secret Santa assignments.")

if __name__ == "__main__":
    print("=" * 60)
    print("Quiz Questions Setup")
    print("=" * 60)
    
    try:
        add_questions_to_db()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
