from database import create_secret_santa_assignments, get_all_users, initialize_default_questions

def main():
    """Admin script to set up Secret Santa assignments"""
    
    print("=" * 50)
    print("Secret Santa Admin Setup")
    print("=" * 50)
    
    # Initialize default questions if needed
    print("\n1. Initializing default questions...")
    try:
        initialize_default_questions()
        print("   ✓ Questions initialized")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Get all users
    print("\n2. Fetching users...")
    users = get_all_users()
    print(f"   Total registered users: {len(users)}")
    
    if len(users) < 2:
        print("   ✗ Need at least 2 users to create assignments")
        print("   Please wait for more users to register")
        return
    
    # Display users
    print("\n   Registered users:")
    for user in users:
        status = "✓" if user.get('profile_completed') else "✗"
        print(f"   {status} {user['username']} ({user['email']})")
    
    # Create assignments
    print("\n3. Creating Secret Santa assignments...")
    confirm = input("   Proceed with assignment creation? (yes/no): ")
    
    if confirm.lower() == 'yes':
        success, message = create_secret_santa_assignments(None)
        if success:
            print(f"   ✓ {message}")
            print("\n🎄 Setup complete! Users can now reveal their assignments.")
        else:
            print(f"   ✗ {message}")
    else:
        print("   Assignment creation cancelled")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
