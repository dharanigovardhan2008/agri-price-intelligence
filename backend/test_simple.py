"""Simple Firebase Test"""

import os
import sys

# Set environment
os.environ['FIREBASE_CREDENTIALS_PATH'] = os.path.join('..', 'firebase', 'firebase-config.json')

print("Testing Firebase...")

try:
    from services.firebase_service import firebase_service
    print("✅ Firebase connected successfully!")
    print(f"   Database: {firebase_service.db}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nMake sure you have:")
    print("1. Downloaded firebase-config.json from Firebase Console")
    print("2. Placed it in: firebase/firebase-config.json")