"""
Database Verification Script for Secret Santa App
This script shows current database status without making any changes
Run this to check what data exists before cleaning
"""

from firebase_config import get_db

def count_documents(collection_name):
    """Count documents in a collection and show sample IDs"""
    db = get_db()
    collection_ref = db.collection(collection_name)
    
    docs = list(collection_ref.stream())
    count = len(docs)
    
    if count > 0:
        print(f"\n  📊 {collection_name}: {count} document(s)")
        print(f"     Sample IDs: {', '.join([doc.id for doc in docs[:5]])}")
        if count > 5:
            print(f"     ... and {count - 5} more")
    else:
        print(f"\n  📊 {collection_name}: Empty")
    
    return count

def verify_database():
    """Show current database status"""
    print("=" * 60)
    print("SECRET SANTA DATABASE STATUS")
    print("=" * 60)
    
    collections = ['users', 'profiles', 'questions', 'assignments']
    
    total_docs = 0
    for collection in collections:
        try:
            count = count_documents(collection)
            total_docs += count
        except Exception as e:
            print(f"\n  ❌ Error reading {collection}: {e}")
    
    print("\n" + "=" * 60)
    print(f"Total documents across all collections: {total_docs}")
    print("=" * 60)
    
    if total_docs > 0:
        print("\n💡 TIP: Run 'python clean_database.py' to remove test data")
    else:
        print("\n✅ Database is empty and ready for production!")

if __name__ == "__main__":
    try:
        verify_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
