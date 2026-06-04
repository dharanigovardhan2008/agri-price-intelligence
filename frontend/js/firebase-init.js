// Firebase Initialization for Frontend
// Import Firebase SDK from CDN in your HTML first

// Import config
import firebaseConfig from '../../../firebase/firebase-web-config.js';

// Initialize Firebase
let app;
let db;
let auth;
let storage;

try {
  // Check if Firebase is loaded
  if (typeof firebase === 'undefined') {
    console.error('❌ Firebase SDK not loaded. Add Firebase scripts to HTML.');
    throw new Error('Firebase SDK not loaded');
  }

  // Initialize Firebase App
  app = firebase.initializeApp(firebaseConfig);
  
  // Initialize services
  db = firebase.firestore();
  auth = firebase.auth();
  storage = firebase.storage();
  
  console.log('✅ Firebase initialized successfully');
  console.log('📊 Project ID:', firebaseConfig.projectId);
  
  // Optional: Enable offline persistence
  db.enablePersistence()
    .then(() => {
      console.log('✅ Offline persistence enabled');
    })
    .catch((err) => {
      if (err.code === 'failed-precondition') {
        console.warn('⚠️ Multiple tabs open, persistence available in first tab only');
      } else if (err.code === 'unimplemented') {
        console.warn('⚠️ Browser doesn\'t support persistence');
      }
    });

} catch (error) {
  console.error('❌ Firebase initialization error:', error);
}

// Export services
export { app, db, auth, storage, firebaseConfig };

// For non-module browsers
if (typeof window !== 'undefined') {
  window.Firebase = {
    app,
    db,
    auth,
    storage,
    config: firebaseConfig
  };
}