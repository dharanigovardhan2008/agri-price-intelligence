// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBHLF-2HqkaoWT9e2ocyHhQJpuAa-0_8f0",
  authDomain: "sell-intelligence.firebaseapp.com",
  projectId: "sell-intelligence",
  storageBucket: "sell-intelligence.firebasestorage.app",
  messagingSenderId: "93266050830",
  appId: "1:93266050830:web:6d5eeb731e150f2c7a615f",
  measurementId: "G-4M2955KEE9"
};

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = firebaseConfig;
}

// For browser direct use
if (typeof window !== 'undefined') {
  window.firebaseConfig = firebaseConfig;
}