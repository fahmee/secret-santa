# 🔥 Firebase Setup Guide

## Step 1: Generate Service Account Key

You're currently on the Service Accounts page. Here's what to do:

### Option 1: Generate New Private Key (Recommended)

1. **Scroll down** on the Service Accounts page
2. Look for a button that says **"Generate new private key"**
3. Click it
4. A dialog will appear warning you to keep the key secure
5. Click **"Generate key"**
6. A JSON file will download automatically (e.g., `secret-santa-c5874-firebase-adminsdk-xxxxx.json`)

### Option 2: Use Python SDK Configuration

If you prefer Python configuration, follow these steps:

1. Click on **"Python"** radio button (shown in your screenshot)
2. You'll see a code snippet like:
   ```python
   var admin = require("firebase-admin");
   ```
3. Below that, there should be a **"Generate new private key"** button

## Step 2: Save the Service Account Key

Once you download the JSON file:

1. **Rename it** to `serviceAccountKey.json`
2. **Move it** to your project folder: `c:\Users\fahahmad\Documents\secretSanta\`
3. **IMPORTANT**: Never commit this file to Git (it's already in `.gitignore`)

## Step 3: Verify the JSON Structure

Your `serviceAccountKey.json` should look like this:

```json
{
  "type": "service_account",
  "project_id": "secret-santa-c5874",
  "private_key_id": "xxxxxxxxxxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@secret-santa-c5874.iam.gserviceaccount.com",
  "client_id": "xxxxxxxxxxxxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

## Step 4: Enable Firestore Database

1. In Firebase Console, go to **"Build"** → **"Firestore Database"**
2. Click **"Create database"**
3. Choose **"Start in test mode"** (for development)
4. Select your preferred location
5. Click **"Enable"**

## Step 5: Set Firestore Security Rules (Optional for now)

For development, you can use these rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;  // WARNING: Only for development!
    }
  }
}
```

**IMPORTANT**: Before going to production, update these rules for security!

## Step 6: Test the Connection

After placing `serviceAccountKey.json` in your project folder, run:

```powershell
python test_firebase.py
```

This will verify your Firebase connection is working.

## Troubleshooting

### Can't find "Generate new private key" button?
- Make sure you're on the **Service accounts** tab
- Scroll down the page - the button is usually below the code snippets
- Try refreshing the page

### Downloaded the wrong file?
- The file should be named like: `secret-santa-xxxxx-firebase-adminsdk-xxxxx.json`
- It should be a JSON file (not a .txt or other format)
- Check your Downloads folder

### Permission errors?
- Make sure you have Owner or Editor role in the Firebase project
- Check the "Users and permissions" tab to verify your access

## Next Steps

Once you have `serviceAccountKey.json` in place:

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run the app: `streamlit run app.py`
3. ✅ Create some test users
4. ✅ Run admin setup: `python admin_setup.py`

---

Need more help? Check the main README.md file!
