# 🎅 Secret Santa Streamlit Application

A festive Secret Santa web application built with Streamlit and Firebase, featuring user authentication, profile management, and an interactive gift assignment reveal system.

## ✨ Features

- **User Authentication**: Secure registration and login system
- **Profile Management**: Users can add shipping address, wishlist, and anti-wishlist
- **Interactive Quiz**: Answer Christmas-themed questions to reveal your Secret Santa assignment
- **Spinner Wheel Animation**: Exciting 8-slot spinner wheel to reveal your gift recipient
- **Firebase Integration**: Real-time database for storing user data and assignments
- **Responsive Design**: Beautiful festive UI with gradient backgrounds and animations

## 📋 Prerequisites

- Python 3.8 or higher
- Firebase account with Firestore database
- Streamlit account (for deployment)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd secretSanta
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Firebase Setup

1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Add project" and follow the setup wizard
   - Enable Firestore Database

2. **Generate Service Account Key**:
   - In Firebase Console, go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `serviceAccountKey.json` in the project root

3. **Configure Firebase**:
   - For local development: Place `serviceAccountKey.json` in the project root
   - For deployment: Use the secrets configuration (see deployment section)

### 4. Configure Streamlit Secrets

Create `.streamlit/secrets.toml` file (copy from `.streamlit/secrets.toml.template`):

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your Firebase credentials from the service account JSON file.

## 🏃 Running Locally

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📊 Database Structure

### Collections

1. **users**
   - `user_id` (string): Unique user identifier
   - `username` (string): User's display name
   - `email` (string): User's email
   - `password` (string): Hashed password
   - `profile_completed` (boolean): Profile completion status
   - `created_at` (timestamp): Account creation time

2. **profiles**
   - `user_id` (string): Reference to user
   - `shipping_address` (string): User's shipping address
   - `wishlist` (string): Items user wants to receive
   - `anti_wishlist` (string): Items user doesn't want
   - `updated_at` (timestamp): Last update time

3. **assignments**
   - `giver_id` (string): User who gives the gift
   - `receiver_id` (string): User who receives the gift
   - `revealed` (boolean): Whether assignment has been revealed
   - `created_at` (timestamp): Assignment creation time

4. **questions**
   - `question` (string): Question text
   - `options` (array): Answer options
   - `correct_answer` (string): The correct answer

## 👨‍💼 Admin Functions

To create Secret Santa assignments, you'll need to run the admin function. Create a file `admin_setup.py`:

```python
from database import create_secret_santa_assignments, get_all_users

# Run this after all users have registered
users = get_all_users()
print(f"Total users: {len(users)}")

if len(users) >= 2:
    success, message = create_secret_santa_assignments(None)
    print(message)
else:
    print("Need at least 2 users to create assignments")
```

Run it with:
```bash
python admin_setup.py
```

## 🌐 Deployment to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository, branch, and main file (`app.py`)
4. Click "Advanced settings"
5. Add your Firebase credentials in the Secrets section:

```toml
[firebase]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYour-Private-Key-Here\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project-id.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "your-cert-url"
```

6. Click "Deploy"

## 🎯 How to Use

### For Users

1. **Register**: Create an account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Complete Profile**: Fill in your shipping address, wishlist, and anti-wishlist
4. **Answer Quiz**: Answer a Christmas-themed question correctly
5. **Spin the Wheel**: Watch the spinner reveal your Secret Santa child
6. **View Details**: See your recipient's profile details and shopping preferences

### For Organizers

1. Wait for all participants to register
2. Run the admin script to generate Secret Santa assignments
3. Notify participants that assignments are ready
4. Monitor the database to ensure all profiles are completed

## 🔒 Security Notes

- Passwords are hashed using SHA-256
- Firebase credentials should NEVER be committed to version control
- Always use `.gitignore` to exclude sensitive files
- Use Streamlit secrets for production deployment

## 🛠️ Troubleshooting

### Firebase Connection Issues
- Verify your service account JSON is correct
- Check that Firestore is enabled in Firebase Console
- Ensure network connectivity to Firebase services

### Assignment Not Found
- Make sure the admin has run the assignment creation script
- Verify there are at least 2 registered users

### Profile Not Saving
- Check browser console for errors
- Verify Firebase write permissions are enabled

## 📝 Future Enhancements

- Email notifications when assignments are ready
- Gift tracking and confirmation
- Multi-year event management
- Custom question creation interface
- Mobile app version

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🎄 Happy Holidays!

Enjoy your Secret Santa gift exchange! 🎁

---

**Created with ❤️ for spreading holiday cheer**
