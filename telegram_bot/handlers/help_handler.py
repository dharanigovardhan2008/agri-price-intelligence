from telegram import Update
from telegram.ext import ContextTypes
from config import LANGUAGES

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    lang = context.user_data.get('language', 'en')
    await update.message.reply_text(
        LANGUAGES[lang]['help'],
        parse_mode='Markdown'
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_text = '''
🌾 *Kisan Price Buddy*

*Version:* 1.0.0
*Made with* ❤️ *for Indian Farmers*

*Data Sources:*
• Agmarknet (APMC Prices)
• Data.gov.in
• Ministry of Agriculture

*Features:*
✅ Real-time price comparison
✅ AI-powered sell/hold recommendations
✅ Profit calculator
✅ Price alerts
✅ Historical trends
✅ Multi-language support

*Support:*
Email: support@kisanprice.com
Telegram: @KisanPriceSupport

*Open Source Project*
Building technology to empower farmers!
    '''
    
    await update.message.reply_text(about_text, parse_mode='Markdown')