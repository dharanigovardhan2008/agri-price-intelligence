"""
Test Firebase Connection
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("🧪 Testing Firebase Connection...")
print("=" * 60)

# Step 1: Check if firebase-admin is installed
print("\n1. Checking firebase-admin module...")
try:
    import firebase_admin
    print(f"   ✅ firebase-admin version: {firebase_admin.__version__}")
except ImportError as e:
    print(f"   ❌ Error: {e}")
    print("\n   Run: pip install firebase-admin")
    sys.exit(1)

# Step 2: Check if config file exists
print("\n2. Checking firebase-config.json...")
config_path = os.path.join(os.path.dirname(__file__), '..', 'firebase', 'firebase-config.json')
if os.path.exists(config_path):
    print(f"   ✅ Config file found: {config_path}")
else:
    print(f"   ❌ Config file not found: {config_path}")
    print("\n   Please download from Firebase Console:")
    print("   Settings → Service Accounts → Generate New Private Key")
    sys.exit(1)

# Step 3: Set environment variable
print("\n3. Setting environment variable...")
os.environ['FIREBASE_CREDENTIALS_PATH'] = config_path
print(f"   ✅ FIREBASE_CREDENTIALS_PATH set")

# Step 4: Import firebase service
print("\n4. Importing Firebase service...")
try:
    from services.firebase_service import firebase_service
    print(f"   ✅ Firebase service imported")
    print(f"   ✅ Database instance: {type(firebase_service.db)}")
except Exception as e:
    print(f"   ❌ Error importing service: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Test database connection
print("\n5. Testing database connection...")
try:
    # Try to list collections
    collections = firebase_service.db.collections()
    collection_names = [col.id for col in collections]
    print(f"   ✅ Connected to Firestore")
    print(f"   📂 Collections: {collection_names if collection_names else '(none yet)'}")
except Exception as e:
    print(f"   ❌ Error connecting to database: {e}")
    sys.exit(1)

# Step 6: Test read/write
print("\n6. Testing read/write operations...")
try:
    # Write test document
    test_ref = firebase_service.db.collection('_test').document('connection_test')
    test_ref.set({
        'test': True,
        'timestamp': firebase_admin.firestore.SERVER_TIMESTAMP,
        'message': 'Connection test successful'
    })
    print(f"   ✅ Write test passed")
    
    # Read test document
    doc = test_ref.get()
    if doc.exists:
        print(f"   ✅ Read test passed")
        print(f"   📄 Document data: {doc.to_dict()}")
    
    # Delete test document
    test_ref.delete()
    print(f"   ✅ Delete test passed")
    
except Exception as e:
    print(f"   ❌ Error in operations: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 All Firebase tests passed!")
print("=" * 60)
print("\n✅ Your Firebase is configured correctly and ready to use!")