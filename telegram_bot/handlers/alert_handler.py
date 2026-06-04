from telegram import Update
from telegram.ext import ContextTypes
import requests
from config import API_BASE_URL, LANGUAGES

async def alert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /alert command"""
    try:
        if len(context.args) < 2:
            await update.message.reply_text(
                '*Set Price Alert*\n\n*Usage:*\n`/alert <commodity> <price>`\n\n*Example:*\n`/alert wheat 2200`\n\nI will notify you when the price reaches ₹2200',
                parse_mode='Markdown'
            )
            return
        
        commodity = context.args[0].capitalize()
        target_price = float(context.args[1])
        user_id = update.effective_user.id
        
        # Get user data
        user_response = requests.get(f"{API_BASE_URL}/auth/user/telegram/{user_id}")
        
        if user_response.status_code != 200:
            await update.message.reply_text(
                '❌ Please register first using /start',
                parse_mode='Markdown'
            )
            return
        
        user_data = user_response.json()
        
        # Create alert
        alert_data = {
            'userId': user_data.get('userId', ''),
            'commodity': commodity,
            'targetPrice': target_price,
            'alertType': 'price_above'
        }
        
        response = requests.post(f"{API_BASE_URL}/alerts/create", json=alert_data)
        
        if response.status_code == 201:
            await update.message.reply_text(
                f"✅ *Alert Set Successfully!*\n\n"
                f"🌾 Commodity: *{commodity}*\n"
                f"💰 Target Price: *₹{target_price}*\n\n"
                f"I'll notify you when {commodity} price reaches or exceeds ₹{target_price} in your area.\n\n"
                f"Use /myalerts to view all alerts.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                '❌ Error creating alert. Please try again.',
                parse_mode='Markdown'
            )
            
    except ValueError:
        await update.message.reply_text(
            '❌ Invalid price. Please enter a number.\n\nExample: `/alert wheat 2200`',
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"Error in alert command: {e}")
        await update.message.reply_text(
            '❌ An error occurred. Please try again.',
            parse_mode='Markdown'
        )

async def myalerts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's alerts"""
    try:
        user_id = update.effective_user.id
        
        # Get user data
        user_response = requests.get(f"{API_BASE_URL}/auth/user/telegram/{user_id}")
        
        if user_response.status_code != 200:
            await update.message.reply_text(
                '❌ Please register first using /start',
                parse_mode='Markdown'
            )
            return
        
        user_data = user_response.json()
        
        # Get alerts
        response = requests.get(f"{API_BASE_URL}/alerts/user/{user_data.get('userId', '')}")
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            if not alerts:
                await update.message.reply_text(
                    '📭 *No Active Alerts*\n\nYou don\'t have any price alerts set.\n\nCreate one using:\n`/alert wheat 2200`',
                    parse_mode='Markdown'
                )
                return
            
            message = f"🔔 *Your Active Alerts ({len(alerts)})*\n\n"
            
            for i, alert in enumerate(alerts, 1):
                message += f"*{i}. {alert['commodity']}*\n"
                message += f"   Target: ₹{alert['targetPrice']}\n"
                message += f"   Type: {alert['alertType']}\n\n"
            
            message += "\n_To delete an alert, contact @KisanPriceSupport_"
            
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                '❌ Error fetching alerts.',
                parse_mode='Markdown'
            )
            
    except Exception as e:
        print(f"Error in myalerts command: {e}")
        await update.message.reply_text(
            '❌ An error occurred. Please try again.',
            parse_mode='Markdown'
        )