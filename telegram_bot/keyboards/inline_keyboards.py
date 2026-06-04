from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import STATES, COMMODITIES

def get_language_keyboard():
    """Language selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("English 🇬🇧", callback_data='lang_en'),
            InlineKeyboardButton("हिंदी 🇮🇳", callback_data='lang_hi')
        ],
        [
            InlineKeyboardButton("ਪੰਜਾਬੀ 🇮🇳", callback_data='lang_pa'),
            InlineKeyboardButton("தமிழ் 🇮🇳", callback_data='lang_ta')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_state_keyboard():
    """State selection keyboard"""
    keyboard = []
    
    # Create rows of 2 buttons each
    for i in range(0, len(STATES), 2):
        row = []
        row.append(InlineKeyboardButton(STATES[i], callback_data=f'state_{STATES[i]}'))
        if i + 1 < len(STATES):
            row.append(InlineKeyboardButton(STATES[i + 1], callback_data=f'state_{STATES[i + 1]}'))
        keyboard.append(row)
    
    return InlineKeyboardMarkup(keyboard)

def get_commodity_keyboard():
    """Commodity selection keyboard"""
    keyboard = []
    
    # Create rows of 2 buttons each
    for i in range(0, len(COMMODITIES), 2):
        row = []
        row.append(InlineKeyboardButton(
            f"{COMMODITIES[i]} 🌾", 
            callback_data=f'crop_{COMMODITIES[i]}'
        ))
        if i + 1 < len(COMMODITIES):
            row.append(InlineKeyboardButton(
                f"{COMMODITIES[i + 1]} 🌾", 
                callback_data=f'crop_{COMMODITIES[i + 1]}'
            ))
        keyboard.append(row)
    
    # Add "Other" option
    keyboard.append([InlineKeyboardButton("➕ Other Crop", callback_data='crop_other')])
    
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard(lang='en'):
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("🌾 I Want to Sell", callback_data='menu_sell')],
        [InlineKeyboardButton("💰 Check Prices", callback_data='menu_prices')],
        [InlineKeyboardButton("📊 Price Trends", callback_data='menu_trends')],
        [InlineKeyboardButton("🔔 My Alerts", callback_data='menu_alerts')],
        [InlineKeyboardButton("📜 History", callback_data='menu_history')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='menu_settings')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_decision_keyboard():
    """Decision action keyboard"""
    keyboard = [
        [InlineKeyboardButton("🔔 Set Price Alert", callback_data='action_alert')],
        [InlineKeyboardButton("📍 Get Directions", callback_data='action_directions')],
        [InlineKeyboardButton("📊 Detailed Report", callback_data='action_detailed')],
        [InlineKeyboardButton("↩️ Main Menu", callback_data='action_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard():
    """Yes/No confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes", callback_data='confirm_yes'),
            InlineKeyboardButton("❌ No", callback_data='confirm_no')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)