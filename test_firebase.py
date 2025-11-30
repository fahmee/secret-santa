"""
Test script to verify Firebase connection
Run this after setting up your serviceAccountKey.json file
"""

import os
import sys

def test_firebase_connection():
    print("=" * 60)
    print("Firebase Connection Test")
    print("=" * 60)
    
    # Check if service account key exists
    print("\n1. Checking for service account key file...")
    if os.path.exists('serviceAccountKey.json'):
        print("   ✅ serviceAccountKey.json found!")
    else:
        print("   ❌ serviceAccountKey.json NOT found!")
        print("\n   Please download your service account key from Firebase:")
        print("   1. Go to Firebase Console")
        print("   2. Project Settings > Service Accounts")
        print("   3. Click 'Generate new private key'")
        print("   4. Save as 'serviceAccountKey.json' in this folder")
        return False
    
    # Try to import Firebase modules
    print("\n2. Checking Firebase Admin SDK installation...")
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        print("   ✅ Firebase Admin SDK installed!")
    except ImportError as e:
        print(f"   ❌ Firebase Admin SDK not installed!")
        print(f"   Error: {e}")
        print("\n   Please run: pip install -r requirements.txt")
        return False
    
    # Try to initialize Firebase
    print("\n3. Attempting to initialize Firebase...")
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        print("   ✅ Firebase initialized successfully!")
    except Exception as e:
        print(f"   ❌ Failed to initialize Firebase!")
        print(f"   Error: {e}")
        return False
    
    # Try to connect to Firestore
    print("\n4. Connecting to Firestore database...")
    try:
        db = firestore.client()
        print("   ✅ Connected to Firestore!")
    except Exception as e:
        print(f"   ❌ Failed to connect to Firestore!")
        print(f"   Error: {e}")
        print("\n   Make sure you've enabled Firestore in Firebase Console:")
        print("   Build > Firestore Database > Create Database")
        return False
    
    # Try a simple read operation
    print("\n5. Testing database read operation...")
    try:
        # Try to read from users collection (won't fail even if empty)
        users_ref = db.collection('users')
        users = list(users_ref.limit(1).stream())
        print(f"   ✅ Database read successful!")
        print(f"   Found {len(users)} user(s) in database")
    except Exception as e:
        print(f"   ❌ Failed to read from database!")
        print(f"   Error: {e}")
        return False
    
    # Try a simple write operation
    print("\n6. Testing database write operation...")
    try:
        test_ref = db.collection('_test').document('connection_test')
        test_ref.set({
            'test': True,
            'message': 'Firebase connection successful!',
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("   ✅ Database write successful!")
        
        # Clean up test document
        test_ref.delete()
        print("   ✅ Test document cleaned up")
    except Exception as e:
        print(f"   ❌ Failed to write to database!")
        print(f"   Error: {e}")
        print("\n   Check your Firestore security rules:")
        print("   Make sure writes are allowed in test mode")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Firebase is configured correctly!")
    print("=" * 60)
    print("\nYou can now:")
    print("  • Run the app: streamlit run app.py")
    print("  • Create test users and profiles")
    print("  • Run admin setup: python admin_setup.py")
    print("\n" + "=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_firebase_connection()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
