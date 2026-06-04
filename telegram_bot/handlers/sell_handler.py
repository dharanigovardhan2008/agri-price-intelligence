from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from keyboards.inline_keyboards import get_commodity_keyboard, get_decision_keyboard
import requests
from config import API_BASE_URL, LANGUAGES
from utils.formatters import format_recommendation_message
import sys
sys.path.append('..')

# Conversation states
CROP, QUANTITY, COST = range(3)

async def sell_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start sell conversation"""
    query = update.callback_query if update.callback_query else None
    
    if query:
        await query.answer()
    
    lang = context.user_data.get('language', 'en')
    message = LANGUAGES[lang]['sell_commodity']
    
    if query:
        await query.edit_message_text(
            message,
            reply_markup=get_commodity_keyboard(),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            message,
            reply_markup=get_commodity_keyboard(),
            parse_mode='Markdown'
        )
    
    return CROP

async def crop_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle crop selection"""
    query = update.callback_query
    await query.answer()
    
    crop_data = query.data.split('_')
    
    if crop_data[1] == 'other':
        lang = context.user_data.get('language', 'en')
        await query.edit_message_text(
            '🌾 Please type the crop name:',
            parse_mode='Markdown'
        )
        return CROP
    
    crop = crop_data[1]
    context.user_data['sell_crop'] = crop
    
    lang = context.user_data.get('language', 'en')
    
    await query.edit_message_text(
        f"✅ Selected: *{crop}*\n\n{LANGUAGES[lang]['enter_quantity']}",
        parse_mode='Markdown'
    )
    return QUANTITY

async def crop_typed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle manually typed crop name"""
    crop = update.message.text
    context.user_data['sell_crop'] = crop
    
    lang = context.user_data.get('language', 'en')
    
    await update.message.reply_text(
        f"✅ Selected: *{crop}*\n\n{LANGUAGES[lang]['enter_quantity']}",
        parse_mode='Markdown'
    )
    return QUANTITY

async def quantity_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quantity entry"""
    try:
        quantity = float(update.message.text)
        context.user_data['sell_quantity'] = quantity
        
        lang = context.user_data.get('language', 'en')
        
        await update.message.reply_text(
            f"✅ Quantity: *{quantity} quintals*\n\n{LANGUAGES[lang]['enter_cost']}",
            parse_mode='Markdown'
        )
        return COST
        
    except ValueError:
        await update.message.reply_text(
            '❌ Invalid number. Please enter a valid quantity:',
            parse_mode='Markdown'
        )
        return QUANTITY

async def cost_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cost entry"""
    try:
        cost = float(update.message.text)
        context.user_data['sell_cost'] = cost
        
        lang = context.user_data.get('language', 'en')
        
        # Show analyzing message
        analyzing_msg = await update.message.reply_text(
            LANGUAGES[lang]['analyzing'],
            parse_mode='Markdown'
        )
        
        # Get recommendation
        await get_sell_recommendation(update, context, analyzing_msg)
        
        return ConversationHandler.END
        
    except ValueError:
        await update.message.reply_text(
            '❌ Invalid amount. Please enter cost per quintal in ₹:',
            parse_mode='Markdown'
        )
        return COST

async def get_sell_recommendation(update: Update, context: ContextTypes.DEFAULT_TYPE, analyzing_msg):
    """Get sell recommendation from API"""
    user_id = update.effective_user.id
    lang = context.user_data.get('language', 'en')
    
    try:
        # Get user data
        user_response = requests.get(f"{API_BASE_URL}/auth/user/telegram/{user_id}")
        
        if user_response.status_code != 200:
            await analyzing_msg.edit_text(
                '❌ User not found. Please use /start to register.',
                parse_mode='Markdown'
            )
            return
        
        user_data = user_response.json()
        
        # Prepare request
        sell_data = {
            'commodity': context.user_data['sell_crop'],
            'quantity': context.user_data['sell_quantity'],
            'costPerQuintal': context.user_data['sell_cost'],
            'userLocation': {
                'state': user_data.get('location', {}).get('state', 'Punjab'),
                'lat': 30.7051,
                'lng': 76.2220
            },
            'userId': user_data.get('userId', '')
        }
        
        # Get recommendation
        response = requests.post(
            f"{API_BASE_URL}/sell/analyze",
            json=sell_data,
            timeout=30
        )
        
        if response.status_code == 200:
            recommendation = response.json()
            message = format_recommendation_message(recommendation, lang)
            
            await analyzing_msg.edit_text(
                message,
                parse_mode='Markdown',
                reply_markup=get_decision_keyboard()
            )
        else:
            error_data = response.json()
            await analyzing_msg.edit_text(
                f"❌ {error_data.get('error', 'Analysis failed')}",
                parse_mode='Markdown'
            )
            
    except requests.exceptions.Timeout:
        await analyzing_msg.edit_text(
            '❌ Request timed out. Please try again.',
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error getting recommendation: {e}")
        await analyzing_msg.edit_text(
            LANGUAGES[lang]['error'],
            parse_mode='Markdown'
        )

async def handle_decision_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle decision action buttons"""
    query = update.callback_query
    await query.answer()
    
    action = query.data.split('_')[1]
    
    if action == 'alert':
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            '✅ *Alert Set!*\n\nI will notify you when:\n• Price goes higher\n• Better opportunity appears\n\nUse /myalerts to manage alerts.',
            parse_mode='Markdown'
        )
    elif action == 'directions':
        await query.answer('Opening Google Maps...', show_alert=True)
    elif action == 'detailed':
        await query.answer('Showing detailed analysis...', show_alert=True)
    elif action == 'cancel':
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text('Operation cancelled.')