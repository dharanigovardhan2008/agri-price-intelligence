from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards.inline_keyboards import get_language_keyboard, get_state_keyboard, get_main_menu_keyboard
import requests
from config import API_BASE_URL, LANGUAGES
import sys
sys.path.append('..')

# Conversation states
LANGUAGE, STATE, DISTRICT = range(3)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    telegram_id = user.id
    
    try:
        # Check if user exists
        response = requests.get(f"{API_BASE_URL}/auth/user/telegram/{telegram_id}")
        
        if response.status_code == 200:
            # User exists
            user_data = response.json()
            lang = user_data.get('language', 'en')
            
            await update.message.reply_text(
                LANGUAGES[lang]['profile_setup'],
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
            return ConversationHandler.END
        else:
            # New user - start registration
            await update.message.reply_text(
                LANGUAGES['en']['welcome'],
                parse_mode='Markdown'
            )
            await update.message.reply_text(
                LANGUAGES['en']['choose_language'],
                reply_markup=get_language_keyboard()
            )
            return LANGUAGE
            
    except Exception as e:
        print(f"Error in start command: {e}")
        await update.message.reply_text(
            LANGUAGES['en']['error'],
            parse_mode='Markdown'
        )
        return ConversationHandler.END

async def language_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection"""
    query = update.callback_query
    await query.answer()
    
    lang = query.data.split('_')[1]
    context.user_data['language'] = lang
    
    await query.edit_message_text(
        LANGUAGES[lang]['select_state'],
        reply_markup=get_state_keyboard()
    )
    return STATE

async def state_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle state selection"""
    query = update.callback_query
    await query.answer()
    
    state = query.data.split('_')[1]
    context.user_data['state'] = state
    
    lang = context.user_data.get('language', 'en')
    
    await query.edit_message_text(
        LANGUAGES[lang]['select_district']
    )
    return DISTRICT

async def district_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle district entry"""
    district = update.message.text
    context.user_data['district'] = district
    
    user = update.effective_user
    lang = context.user_data.get('language', 'en')
    
    # Create user in database
    user_data = {
        'name': user.full_name,
        'phone': '',
        'telegramId': str(user.id),
        'state': context.user_data['state'],
        'district': district,
        'language': lang
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=user_data
        )
        
        if response.status_code == 201:
            await update.message.reply_text(
                LANGUAGES[lang]['profile_setup'],
                reply_markup=get_main_menu_keyboard(lang),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                LANGUAGES[lang]['error'],
                parse_mode='Markdown'
            )
            
    except Exception as e:
        print(f"Error creating user: {e}")
        await update.message.reply_text(
            LANGUAGES[lang]['error'],
            parse_mode='Markdown'
        )
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        '❌ Cancelled. Type /start to begin again.',
        parse_mode='Markdown'
    )
    return ConversationHandler.END