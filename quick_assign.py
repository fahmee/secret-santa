"""Quick script to create assignments without prompts"""
from database import create_secret_santa_assignments, get_all_users

print("Checking users...")
users = get_all_users()
print(f"Found {len(users)} users")

if len(users) >= 2:
    print("Creating assignments...")
    success, message = create_secret_santa_assignments(None)
    print(message)
    if success:
        print("✅ Done! Refresh your browser.")
else:
    print(f"❌ Need at least 2 users, but only found {len(users)}")
    print("Please register more users first.")
