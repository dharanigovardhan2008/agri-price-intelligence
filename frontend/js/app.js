// Main Application JavaScript

const API_BASE_URL = 'https://agri-price-backend-p4yw.onrender.com/api';

// Utility: Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0
    }).format(amount);
}

// Utility: Format number
function formatNumber(num) {
    return new Intl.NumberFormat('en-IN').format(num);
}

// Utility: Show toast notification
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 1.5rem;">
                ${type === 'success' ? '✅' : type === 'error' ? '❌' : '⚠️'}
            </span>
            <span style="font-weight: 500;">${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Utility: Fetch API with error handling
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'API request failed');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        showToast(error.message || 'An error occurred', 'error');
        throw error;
    }
}

// Check API health on load
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
        if (response.ok) {
            console.log('✅ API is healthy');
        } else {
            console.warn('⚠️ API health check failed');
        }
    } catch (error) {
        console.error('❌ API is not responding:', error);
        showToast('Backend server is not running', 'error');
    }
});

// Voice input support
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    window.startVoiceInput = function(inputId) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.lang = 'en-IN';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById(inputId).value = transcript;
            showToast('Voice input captured', 'success');
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            showToast('Voice input failed', 'error');
        };
        
        recognition.start();
        showToast('Listening...', 'info');
    };
}

// Get user's location
function getUserLocation() {
    return new Promise((resolve, reject) => {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                position => {
                    resolve({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    });
                },
                error => {
                    console.error('Geolocation error:', error);
                    // Default to Punjab coordinates
                    resolve({ lat: 30.7051, lng: 76.2220 });
                }
            );
        } else {
            // Default to Punjab coordinates
            resolve({ lat: 30.7051, lng: 76.2220 });
        }
    });
}

// Loading overlay
function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove('hidden');
    }
}

function hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add('hidden');
    }
}

// Export utilities
window.AppUtils = {
    formatCurrency,
    formatNumber,
    showToast,
    fetchAPI,
    getUserLocation,
    showLoading,
    hideLoading
};
