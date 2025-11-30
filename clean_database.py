"""
Clean Database Script for Secret Santa App
This script removes all test data from Firebase Firestore
Run this before deploying to production to ensure a clean database
"""

from firebase_config import get_db
import sys

def clean_collection(collection_name):
    """Delete all documents in a collection"""
    db = get_db()
    collection_ref = db.collection(collection_name)
    
    # Get all documents
    docs = collection_ref.stream()
    deleted_count = 0
    
    for doc in docs:
        doc.reference.delete()
        deleted_count += 1
        print(f"  Deleted: {doc.id}")
    
    return deleted_count

def clean_database():
    """Clean all collections in the database"""
    print("=" * 60)
    print("SECRET SANTA DATABASE CLEANUP")
    print("=" * 60)
    print("\nWARNING: This will delete ALL data from the following collections:")
    print("  - users (all registered users)")
    print("  - profiles (all user profiles with addresses and wishlists)")
    print("  - assignments (all Secret Santa assignments)")
    print("\nThe 'questions' collection will NOT be deleted (quiz questions are preserved)")
    print("=" * 60)
    
    # Confirmation
    response = input("\nAre you sure you want to proceed? Type 'YES' to confirm: ")
    
    if response != "YES":
        print("\n❌ Database cleanup cancelled.")
        sys.exit(0)
    
    print("\n🧹 Starting database cleanup...\n")
    
    # Collections to clean
    collections_to_clean = ['users', 'profiles', 'assignments']
    
    total_deleted = 0
    for collection in collections_to_clean:
        print(f"Cleaning '{collection}' collection...")
        count = clean_collection(collection)
        total_deleted += count
        print(f"  ✅ Deleted {count} document(s) from '{collection}'\n")
    
    print("=" * 60)
    print(f"✅ CLEANUP COMPLETE!")
    print(f"Total documents deleted: {total_deleted}")
    print("\n📝 NOTE: Quiz questions have been preserved.")
    print("🚀 Your database is now ready for production!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        clean_database()
    except KeyboardInterrupt:
        print("\n\n❌ Cleanup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        sys.exit(1)
