import firebase_admin
from firebase_admin import credentials, firestore, auth
import streamlit as st
import json
import os

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    if not firebase_admin._apps:
        try:
            # Try to get from local file first (for development)
            if os.path.exists('serviceAccountKey.json'):
                cred = credentials.Certificate('serviceAccountKey.json')
            # Try to get credentials from Streamlit secrets (for deployment)
            elif hasattr(st, 'secrets') and 'firebase' in st.secrets:
                firebase_credentials = dict(st.secrets['firebase'])
                cred = credentials.Certificate(firebase_credentials)
            else:
                st.error("Firebase credentials not found. Please configure your Firebase credentials.")
                st.stop()
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error initializing Firebase: {str(e)}")
            st.stop()
    
    return firestore.client()

def get_db():
    """Get Firestore database instance"""
    return initialize_firebase()
