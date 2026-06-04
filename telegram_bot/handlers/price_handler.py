from telegram import Update
from telegram.ext import ContextTypes
import requests
from config import API_BASE_URL, LANGUAGES

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /price command"""
    try:
        lang = context.user_data.get('language', 'en')
        
        if len(context.args) < 1:
            await update.message.reply_text(
                '*Usage:*\n`/price <commodity> [state]`\n\n*Example:*\n`/price wheat punjab`',
                parse_mode='Markdown'
            )
            return
        
        commodity = context.args[0].capitalize()
        state = context.args[1].capitalize() if len(context.args) > 1 else 'Punjab'
        
        # Show loading message
        loading_msg = await update.message.reply_text(
            f'🔍 Fetching *{commodity}* prices in *{state}*...',
            parse_mode='Markdown'
        )
        
        # Fetch prices
        response = requests.get(
            f"{API_BASE_URL}/prices/current",
            params={'commodity': commodity, 'state': state}
        )
        
        if response.status_code == 200:
            data = response.json()
            prices = data.get('prices', [])
            
            if not prices:
                await loading_msg.edit_text(
                    f'❌ No prices found for *{commodity}* in *{state}*',
                    parse_mode='Markdown'
                )
                return
            
            # Sort by price (highest first)
            prices.sort(key=lambda x: x['price'], reverse=True)
            
            message = f"💰 *{commodity} Prices in {state}*\n"
            message += f"📅 Date: {prices[0]['date']}\n\n"
            
            for i, price in enumerate(prices[:8], 1):  # Show top 8
                message += f"*{i}. {price['market']}*\n"
                message += f"   💵 ₹{price['price']}/quintal\n"
                message += f"   📦 Arrival: {price.get('arrival', 0)} quintals\n\n"
            
            if len(prices) > 8:
                message += f"_...and {len(prices) - 8} more markets_\n\n"
            
            # Add statistics
            avg_price = sum(p['price'] for p in prices) / len(prices)
            max_price = max(p['price'] for p in prices)
            min_price = min(p['price'] for p in prices)
            
            message += f"📊 *Statistics:*\n"
            message += f"Highest: ₹{max_price}\n"
            message += f"Lowest: ₹{min_price}\n"
            message += f"Average: ₹{avg_price:.2f}\n"
            
            await loading_msg.edit_text(message, parse_mode='Markdown')
        else:
            await loading_msg.edit_text(
                '❌ Error fetching prices. Please try again later.',
                parse_mode='Markdown'
            )
            
    except Exception as e:
        print(f"Error in price command: {e}")
        await update.message.reply_text(
            '❌ An error occurred. Please try again.',
            parse_mode='Markdown'
        )

async def markets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /markets command"""
    try:
        if len(context.args) < 1:
            await update.message.reply_text(
                '*Usage:*\n`/markets <state>`\n\n*Example:*\n`/markets punjab`',
                parse_mode='Markdown'
            )
            return
        
        state = ' '.join(context.args).title()
        
        response = requests.get(
            f"{API_BASE_URL}/prices/markets",
            params={'state': state}
        )
        
        if response.status_code == 200:
            data = response.json()
            markets = data.get('markets', [])
            
            if not markets:
                await update.message.reply_text(
                    f'❌ No markets found for *{state}*',
                    parse_mode='Markdown'
                )
                return
            
            message = f"📍 *Markets in {state}*\n\n"
            
            for market in markets:
                message += f"• *{market['name']}* - {market['district']}\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(
                '❌ Error fetching markets.',
                parse_mode='Markdown'
            )
            
    except Exception as e:
        print(f"Error in markets command: {e}")
        await update.message.reply_text(
            '❌ An error occurred.',
            parse_mode='Markdown'
        )