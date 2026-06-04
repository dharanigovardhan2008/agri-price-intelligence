def format_recommendation_message(rec, lang='en'):
    """Format recommendation message for Telegram"""
    
    decision = rec.get('decision', 'NEUTRAL')
    confidence = rec.get('confidence', 0)
    best_market = rec.get('bestMarket', {})
    
    # Decision emoji and text
    if decision == 'SELL_NOW':
        decision_emoji = '✅'
        decision_text = '*SELL NOW*'
    elif decision == 'WAIT':
        decision_emoji = '⏳'
        decision_text = '*WAIT*'
    else:
        decision_emoji = '📊'
        decision_text = '*NEUTRAL*'
    
    message = f"📊 *ANALYSIS COMPLETE*\n\n"
    message += f"⚡ *RECOMMENDATION:* {decision_emoji} {decision_text}\n"
    message += f"📈 Confidence: {confidence}%\n\n"
    
    # Progress bar for confidence
    filled = int(confidence / 10)
    bar = "█" * filled + "░" * (10 - filled)
    message += f"`{bar}` {confidence}%\n\n"
    
    # Reasoning
    message += "*💡 Why?*\n"
    for reason in rec.get('reasoning', []):
        message += f"  • {reason}\n"
    
    message += f"\n🏆 *BEST MARKET:*\n"
    message += f"📍 *{best_market.get('market_name', 'N/A')}*\n"
    message += f"💰 Price: ₹{best_market.get('price_per_quintal', 0)}/quintal\n"
    message += f"📏 Distance: {best_market.get('distance', 0)} km\n\n"
    
    message += "*💰 PROFIT BREAKDOWN:*\n"
    message += f"```\n"
    message += f"Revenue        ₹{format_number(best_market.get('revenue', 0))}\n"
    message += f"Cost           ₹{format_number(best_market.get('cost', 0))}\n"
    message += f"Transport      ₹{format_number(best_market.get('transport_cost', 0))}\n"
    message += f"Commission     ₹{format_number(best_market.get('commission', 0))}\n"
    message += f"Loading        ₹{format_number(best_market.get('loading_cost', 0))}\n"
    message += f"{'─' * 30}\n"
    message += f"NET PROFIT     ₹{format_number(best_market.get('net_profit', 0))}\n"
    message += f"Margin         {best_market.get('profit_margin', 0):.1f}%\n"
    message += f"```\n"
    
    # Alternative markets
    alt_markets = rec.get('alternativeMarkets', [])
    if alt_markets:
        message += f"\n📍 *OTHER OPTIONS:*\n"
        for i, market in enumerate(alt_markets[:3], 2):
            message += f"{i}. {market['market_name']} - ₹{format_number(market['net_profit'])} profit\n"
    
    # Wait option
    wait_option = rec.get('waitOption')
    if wait_option:
        message += f"\n⏳ *WAIT OPTION:*\n"
        message += f"Wait {wait_option.get('days', 0)} days\n"
        message += f"Expected price: ₹{wait_option.get('expectedPrice', 0)}/quintal\n"
        message += f"Extra profit: ₹{format_number(wait_option.get('potentialExtraProfit', 0))}\n"
        message += f"⚠️ Risk: *{wait_option.get('risk', 'medium').upper()}*\n"
    
    return message

def format_number(num):
    """Format number with Indian number system"""
    try:
        num = float(num)
        if num >= 10000000:  # 1 crore
            return f"{num/10000000:.2f}Cr"
        elif num >= 100000:  # 1 lakh
            return f"{num/100000:.2f}L"
        elif num >= 1000:
            return f"{num/1000:.2f}K"
        else:
            return f"{num:.2f}"
    except:
        return str(num)

def format_currency(amount):
    """Format as Indian currency"""
    return f"₹{format_number(amount)}"