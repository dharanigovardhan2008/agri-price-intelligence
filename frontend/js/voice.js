// Voice Input Handler

class VoiceInput {
    constructor() {
        this.recognition = null;
        this.isSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
        
        if (this.isSupported) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-IN';
        }
    }
    
    start(targetInputId, onResult, onError) {
        if (!this.isSupported) {
            console.warn('Speech recognition not supported');
            return;
        }
        
        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const targetInput = document.getElementById(targetInputId);
            
            if (targetInput) {
                targetInput.value = transcript;
            }
            
            if (onResult) {
                onResult(transcript);
            }
            
            window.AppUtils.showToast('Voice captured: ' + transcript, 'success');
        };
        
        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            
            if (onError) {
                onError(event.error);
            }
            
            window.AppUtils.showToast('Voice input failed', 'error');
        };
        
        this.recognition.onstart = () => {
            window.AppUtils.showToast('🎤 Listening...', 'info');
        };
        
        this.recognition.start();
    }
    
    stop() {
        if (this.recognition) {
            this.recognition.stop();
        }
    }
}

// Export
window.VoiceInput = VoiceInput;

// Add voice button to inputs
function addVoiceButton(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;
    
    const voiceBtn = document.createElement('button');
    voiceBtn.type = 'button';
    voiceBtn.innerHTML = '🎤';
    voiceBtn.style.cssText = `
        position: absolute;
        right: 10px;
        top: 50%;
        transform: translateY(-50%);
        background: #10B981;
        color: white;
        border: none;
        border-radius: 50%;
        width: 36px;
        height: 36px;
        cursor: pointer;
        font-size: 18px;
    `;
    
    const voice = new VoiceInput();
    voiceBtn.onclick = () => voice.start(inputId);
    
    input.parentElement.style.position = 'relative';
    input.style.paddingRight = '50px';
    input.parentElement.appendChild(voiceBtn);
}