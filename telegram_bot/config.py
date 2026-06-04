import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Backend API URL
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000/api')

# Firebase
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS_PATH', '../firebase/firebase-config.json')

# Supported Languages
LANGUAGES = {
    'en': {
        'welcome': '🌾 *Welcome to Kisan Price Buddy!*\n\nI will help you:\n✅ Find best prices across all markets\n✅ Decide when to sell your crops\n✅ Calculate your exact profit\n✅ Send daily price alerts\n\nLet\'s get started!',
        'choose_language': 'Please choose your language:',
        'select_state': 'Select your state:',
        'select_district': 'Enter your district name:',
        'profile_setup': '✅ *Profile setup complete!*\n\nWhat would you like to do?',
        'sell_commodity': '🌾 *What crop do you want to sell?*\n\nSelect from popular crops below or type the name:',
        'enter_quantity': '📦 *How many quintals do you want to sell?*\n\nType a number (e.g., 50)',
        'enter_cost': '💵 *What was your total cost per quintal?*\n\nInclude seeds, fertilizer, labor, etc.\nType amount in ₹ (e.g., 1800)',
        'analyzing': '🔍 *Analyzing market data...*\n\n⏳ Please wait a moment while I:\n• Compare prices across all markets\n• Run AI predictions\n• Calculate your profit scenarios\n\nThis will take 5-10 seconds...',
        'error': '❌ An error occurred. Please try again or contact support.',
        'help': '''
🌾 *Kisan Price Buddy - Help*

*Available Commands:*

/start - Start the bot & setup profile
/sell - Analyze selling decision
/price <crop> [state] - Check current prices
/alert <crop> <price> - Set price alert
/myalerts - View your active alerts
/history - View your analysis history
/help - Show this help message
/cancel - Cancel current operation

*Examples:*
/price wheat punjab
/alert wheat 2200
/sell

*Need Help?*
Contact: @KisanPriceSupport
        '''
    },
    'hi': {
        'welcome': '🌾 *किसान प्राइस बडी में आपका स्वागत है!*\n\nमैं आपकी मदद करूंगा:\n✅ सभी बाजारों में सर्वोत्तम कीमतें खोजें\n✅ अपनी फसल बेचने का समय तय करें\n✅ अपना सटीक लाभ गणना करें\n✅ दैनिक मूल्य अलर्ट भेजें\n\nचलिए शुरू करते हैं!',
        'choose_language': 'कृपया अपनी भाषा चुनें:',
        'select_state': 'अपना राज्य चुनें:',
        'select_district': 'अपने जिले का नाम दर्ज करें:',
        'profile_setup': '✅ *प्रोफ़ाइल सेटअप पूर्ण!*\n\nआप क्या करना चाहेंगे?',
        'sell_commodity': '🌾 *आप कौन सी फसल बेचना चाहते हैं?*\n\nनीचे से चुनें या नाम टाइप करें:',
        'enter_quantity': '📦 *आप कितने क्विंटल बेचना चाहते हैं?*\n\nएक संख्या टाइप करें (उदा. 50)',
        'enter_cost': '💵 *आपकी प्रति क्विंटल कुल लागत क्या थी?*\n\nबीज, खाद, श्रम आदि शामिल करें\n₹ में राशि टाइप करें (उदा. 1800)',
        'analyzing': '🔍 *बाजार डेटा का विश्लेषण कर रहा हूं...*\n\n⏳ कृपया एक क्षण प्रतीक्षा करें जबकि मैं:\n• सभी बाजारों में कीमतों की तुलना करूं\n• AI भविष्यवाणी चलाऊं\n• आपके लाभ परिदृश्यों की गणना करूं\n\nइसमें 5-10 सेकंड लगेंगे...',
        'error': '❌ एक त्रुटि हुई। कृपया पुनः प्रयास करें या सहायता से संपर्क करें।',
        'help': '''
🌾 *किसान प्राइस बडी - मदद*

*उपलब्ध आदेश:*

/start - बॉट शुरू करें और प्रोफ़ाइल सेट करें
/sell - विक्रय विश्लेषण
/price <फसल> [राज्य] - वर्तमान कीमतें जांचें
/alert <फसल> <मूल्य> - मूल्य अलर्ट सेट करें
/myalerts - अपने सक्रिय अलर्ट देखें
/history - अपना विश्लेषण इतिहास देखें
/help - यह सहायता संदेश दिखाएं
/cancel - वर्तमान ऑपरेशन रद्द करें

*उदाहरण:*
/price गेहूं पंजाब
/alert गेहूं 2200
/sell

*मदद चाहिए?*
संपर्क: @KisanPriceSupport
        '''
    },
    'pa': {
        'welcome': '🌾 *ਕਿਸਾਨ ਪ੍ਰਾਈਸ ਬੱਡੀ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ!*\n\nਮੈਂ ਤੁਹਾਡੀ ਮਦਦ ਕਰਾਂਗਾ:\n✅ ਸਾਰੇ ਬਾਜ਼ਾਰਾਂ ਵਿੱਚ ਵਧੀਆ ਕੀਮਤਾਂ ਲੱਭੋ\n✅ ਆਪਣੀ ਫਸਲ ਵੇਚਣ ਦਾ ਸਮਾਂ ਤੈਅ ਕਰੋ\n✅ ਆਪਣਾ ਸਹੀ ਲਾਭ ਗਿਣੋ\n✅ ਰੋਜ਼ਾਨਾ ਕੀਮਤ ਅਲਰਟ ਭੇਜੋ\n\nਚਲੋ ਸ਼ੁਰੂ ਕਰੀਏ!',
        'choose_language': 'ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ:',
        'select_state': 'ਆਪਣਾ ਰਾਜ ਚੁਣੋ:',
        'select_district': 'ਆਪਣੇ ਜ਼ਿਲ੍ਹੇ ਦਾ ਨਾਮ ਦਰਜ ਕਰੋ:',
        'profile_setup': '✅ *ਪ੍ਰੋਫਾਈਲ ਸੈਟਅੱਪ ਪੂਰਾ!*\n\nਤੁਸੀਂ ਕੀ ਕਰਨਾ ਚਾਹੋਗੇ?',
        'sell_commodity': '🌾 *ਤੁਸੀਂ ਕਿਹੜੀ ਫਸਲ ਵੇਚਣਾ ਚਾਹੁੰਦੇ ਹੋ?*\n\nਹੇਠਾਂ ਤੋਂ ਚੁਣੋ ਜਾਂ ਨਾਮ ਟਾਈਪ ਕਰੋ:',
        'enter_quantity': '📦 *ਤੁਸੀਂ ਕਿੰਨੇ ਕੁਇੰਟਲ ਵੇਚਣਾ ਚਾਹੁੰਦੇ ਹੋ?*\n\nਇੱਕ ਨੰਬਰ ਟਾਈਪ ਕਰੋ (ਉਦਾ. 50)',
        'enter_cost': '💵 *ਤੁਹਾਡੀ ਪ੍ਰਤੀ ਕੁਇੰਟਲ ਕੁੱਲ ਲਾਗਤ ਕੀ ਸੀ?*\n\nਬੀਜ, ਖਾਦ, ਮਜ਼ਦੂਰੀ ਆਦਿ ਸ਼ਾਮਲ ਕਰੋ\n₹ ਵਿੱਚ ਰਕਮ ਟਾਈਪ ਕਰੋ (ਉਦਾ. 1800)',
        'analyzing': '🔍 *ਬਾਜ਼ਾਰ ਡੇਟਾ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰ ਰਿਹਾ ਹਾਂ...*\n\n⏳ ਕਿਰਪਾ ਕਰਕੇ ਇੱਕ ਪਲ ਉਡੀਕ ਕਰੋ ਜਦੋਂ ਮੈਂ:\n• ਸਾਰੇ ਬਾਜ਼ਾਰਾਂ ਵਿੱਚ ਕੀਮਤਾਂ ਦੀ ਤੁਲਨਾ ਕਰਦਾ ਹਾਂ\n• AI ਭਵਿੱਖਬਾਣੀ ਚਲਾਉਂਦਾ ਹਾਂ\n• ਤੁਹਾਡੇ ਲਾਭ ਦੀ ਗਣਨਾ ਕਰਦਾ ਹਾਂ\n\nਇਸ ਵਿੱਚ 5-10 ਸਕਿੰਟ ਲੱਗਣਗੇ...',
        'error': '❌ ਇੱਕ ਗਲਤੀ ਹੋਈ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।',
        'help': '🌾 *ਕਿਸਾਨ ਪ੍ਰਾਈਸ ਬੱਡੀ - ਮਦਦ*\n\n/start - ਸ਼ੁਰੂ ਕਰੋ\n/sell - ਵੇਚਣ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ\n/price - ਕੀਮਤਾਂ ਜਾਂਚੋ\n/help - ਮਦਦ'
    }
}

# States list
STATES = [
    'Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 
    'Maharashtra', 'Rajasthan', 'Gujarat', 'Karnataka', 
    'Tamil Nadu', 'Andhra Pradesh', 'Telangana', 'West Bengal'
]

# Popular commodities
COMMODITIES = [
    'Wheat', 'Rice', 'Maize', 'Cotton', 'Potato', 
    'Onion', 'Tomato', 'Bajra', 'Jowar', 'Soybean'
]