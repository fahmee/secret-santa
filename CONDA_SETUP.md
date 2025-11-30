# Secret Santa - Conda Setup Instructions

## Quick Setup for Conda Users

### Step 1: Create a Conda Environment

```powershell
conda create -n secretsanta python=3.10 -y
```

### Step 2: Activate the Environment

```powershell
conda activate secretsanta
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Download Firebase Service Account Key

1. Go to Firebase Console: https://console.firebase.google.com/
2. Select your project: **secret-santa-c5874**
3. Click the gear icon ⚙️ → **Project settings**
4. Go to **Service accounts** tab
5. Scroll down and click **"Generate new private key"**
6. Click **Generate key** in the dialog
7. Save the downloaded JSON file as `serviceAccountKey.json` in this folder

### Step 5: Enable Firestore Database

1. In Firebase Console, go to **Build** → **Firestore Database**
2. Click **Create database**
3. Select **Start in test mode**
4. Choose your region and click **Enable**

### Step 6: Test Firebase Connection

```powershell
python test_firebase.py
```

### Step 7: Run the App

```powershell
streamlit run app.py
```

The app will open in your browser at http://localhost:8501

---

## Troubleshooting

### If conda command not found:
Make sure Conda is in your PATH, or use Anaconda Prompt instead of regular PowerShell.

### If you get module import errors:
Make sure the conda environment is activated:
```powershell
conda activate secretsanta
```

### If Firebase connection fails:
1. Check that `serviceAccountKey.json` exists in the project folder
2. Verify Firestore is enabled in Firebase Console
3. Check the security rules allow read/write (test mode)

---

## Next Steps After App is Running

1. Register 2-3 test users
2. Fill out profiles for each user
3. Run admin script to create assignments:
   ```powershell
   python admin_setup.py
   ```
4. Login as each user to reveal their Secret Santa assignment!
