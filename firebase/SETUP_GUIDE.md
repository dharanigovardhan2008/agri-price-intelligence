# Complete Firebase Configuration Setup

## Step 1: Get Backend Config (Service Account)

### For Python Backend:

1. **Open Firebase Console**
   - Go to https://console.firebase.google.com
   - Select your project

2. **Navigate to Service Accounts**
   - Click ⚙️ (Settings) → Project Settings
   - Click "Service Accounts" tab

3. **Generate Key**
   - Click "Generate New Private Key"
   - Click "Generate Key" button
   - JSON file downloads automatically

4. **Save File**
   - Rename to `firebase-config.json`
   - Move to `firebase/` folder
   - **Format:**
     ```json
     {
       "type": "service_account",
       "project_id": "your-project",
       "private_key_id": "...",
       "private_key": "-----BEGIN PRIVATE KEY-----\n...",
       "client_email": "firebase-adminsdk@...",
       ...
     }
     ```

---

## Step 2: Get Frontend Config (Web App)

### For JavaScript Frontend:

1. **Open Firebase Console**
   - Same project as above

2. **Add Web App**
   - Click "Project Overview"
   - Click `</>` (Web icon)
   - Enter app nickname: "Kisan Price Web"
   - Check "Also set up Firebase Hosting" (optional)
   - Click "Register app"

3. **Copy Configuration**
   - You'll see code like this:
     ```javascript
     const firebaseConfig = {
       apiKey: "AIzaSy...",
       authDomain: "your-project.firebaseapp.com",
       projectId: "your-project",
       storageBucket: "your-project.appspot.com",
       messagingSenderId: "123456789",
       appId: "1:123456789:web:abc123",
       measurementId: "G-XXXXXXXXXX"
     };
     ```

4. **Save Configuration**
   - Create `firebase/firebase-web-config.js`
   - Paste the config:
     ```javascript
     const firebaseConfig = {
       apiKey: "AIzaSy...",
       authDomain: "your-project.firebaseapp.com",
       projectId: "your-project",
       storageBucket: "your-project.appspot.com",
       messagingSenderId: "123456789",
       appId: "1:123456789:web:abc123",
       measurementId: "G-XXXXXXXXXX"
     };
     
     if (typeof module !== 'undefined' && module.exports) {
       module.exports = firebaseConfig;
     }
     
     if (typeof window !== 'undefined') {
       window.firebaseConfig = firebaseConfig;
     }
     ```

---

## Step 3: Update .gitignore

Add to `.gitignore`:

```gitignore
# Firebase credentials
firebase/firebase-config.json
firebase/firebase-web-config.js

# But keep templates
!firebase/*.template.*