import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler
)
from config import BOT_TOKEN

# Import handlers
from handlers.start import (
    start_command, language_selected, state_selected, 
    district_entered, cancel, LANGUAGE, STATE, DISTRICT
)
from handlers.sell_handler import (
    sell_start, crop_selected, crop_typed, quantity_entered, 
    cost_entered, handle_decision_action, CROP, QUANTITY, COST
)
from handlers.price_handler import price_command, markets_command
from handlers.alert_handler import alert_command, myalerts_command
from handlers.help_handler import help_command, about_command

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def menu_handler(update: Update, context):
    """Handle main menu selections"""
    query = update.callback_query
    await query.answer()
    
    menu_item = query.data.split('_')[1]
    
    if menu_item == 'sell':
        await sell_start(update, context)
    elif menu_item == 'prices':
        await query.message.reply_text(
            '💰 *Check Prices*\n\nUse: `/price <crop> [state]`\n\nExample: `/price wheat punjab`',
            parse_mode='Markdown'
        )
    elif menu_item == 'alerts':
        await myalerts_command(update, context)
    elif menu_item == 'history':
        await query.message.reply_text(
            '📜 *Your History*\n\nThis feature is coming soon!',
            parse_mode='Markdown'
        )
    elif menu_item == 'settings':
        await query.message.reply_text(
            '⚙️ *Settings*\n\nThis feature is coming soon!',
            parse_mode='Markdown'
        )

def main():
    """Start the bot"""
    
    if not BOT_TOKEN:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set in environment variables!")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Registration conversation handler
    registration_conv = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            LANGUAGE: [CallbackQueryHandler(language_selected, pattern='^lang_')],
            STATE: [CallbackQueryHandler(state_selected, pattern='^state_')],
            DISTRICT: [MessageHandler(filters.TEXT & ~filters.COMMAND, district_entered)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Sell conversation handler
    sell_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(sell_start, pattern='^menu_sell$'),
            CommandHandler('sell', sell_start)
        ],
        states={
            CROP: [
                CallbackQueryHandler(crop_selected, pattern='^crop_'),
                MessageHandler(filters.TEXT & ~filters.COMMAND, crop_typed)
            ],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity_entered)],
            COST: [MessageHandler(filters.TEXT & ~filters.COMMAND, cost_entered)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Add conversation handlers
    app.add_handler(registration_conv)
    app.add_handler(sell_conv)
    
    # Add command handlers
    app.add_handler(CommandHandler('price', price_command))
    app.add_handler(CommandHandler('markets', markets_command))
    app.add_handler(CommandHandler('alert', alert_command))
    app.add_handler(CommandHandler('myalerts', myalerts_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('about', about_command))
    
    # Add callback query handlers
    app.add_handler(CallbackQueryHandler(menu_handler, pattern='^menu_'))
    app.add_handler(CallbackQueryHandler(handle_decision_action, pattern='^action_'))
    
    # Start bot
    logger.info("🤖 Kisan Price Bot started successfully!")
    logger.info(f"Bot username: @{app.bot.username if hasattr(app.bot, 'username') else 'Unknown'}")
    
    # Run bot
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()