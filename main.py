import os
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes, CallbackQueryHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Constants for dialog states
CHOOSING_SERVICE, ENTERING_PHONE, ENTERING_DEVICE, ENTERING_PROBLEM, CONFIRMING_ORDER = range(5)

# Dictionary of repair services
REPAIR_SERVICES = {
    'battery': {'name': '🔋 Battery Replacement', 'price': 1500},
    'screen': {'name': '📱 Screen Repair', 'price': 3000},
    'charging': {'name': '⚡ Charging Port Repair', 'price': 1200},
    'speaker': {'name': '🔊 Speaker Repair', 'price': 800},
    'button': {'name': '🔘 Button Repair', 'price': 500},
    'water': {'name': '💧 Water Damage Service', 'price': 2000},
    'other': {'name': '🔧 Other', 'price': 0}
}

# Order storage
orders_db = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user = update.effective_user
    welcome_text = f"""👋 Welcome to Phone Repair Service Bot!

I can help you:
📱 Order a phone repair
🔍 Track your order status
💬 Get support

Select an action:
    """
    
    keyboard = [
        ['📋 New Repair Order', '📊 My Orders'],
        ['❓ Help', '📞 Contact']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """📋 **Available Commands:**

/start - Start the bot
/help - Get help
/services - List services
/orders - My orders
/contact - Contact information

**How to order repair:**
1. Press "📋 New Repair Order"
2. Choose service type
3. Enter your phone number
4. Enter device model
5. Describe the problem
6. Confirm order

⏱️ **Processing time:** 1-3 hours
📍 **Address:** 123 Main St, Office 205
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show services list"""
    services_text = "🔧 **Our Services:**\n\n"
    for key, service in REPAIR_SERVICES.items():
        if service['price'] > 0:
            services_text += f"{service['name']} - {service['price']} RUB\n"
    
    await update.message.reply_text(services_text, parse_mode='Markdown')

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contact information"""
    contact_text = """📞 **Contact Info:**

📱 Phone: +7 (999) 123-45-67
💬 Telegram: @phone_repair_service
📧 Email: support@phone-repair.ru
📍 Address: 123 Main St, Office 205

⏰ **Working Hours:**
Mon-Fri: 10:00 - 19:00
Sat: 11:00 - 18:00
Sun: Closed
    """
    await update.message.reply_text(contact_text, parse_mode='Markdown')

async def new_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a new order"""
    keyboard = []
    for key, service in REPAIR_SERVICES.items():
        keyboard.append([InlineKeyboardButton(service['name'], callback_data=f"service_{key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔧 Select repair type:",
        reply_markup=reply_markup
    )
    return CHOOSING_SERVICE

async def service_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle service selection"""
    query = update.callback_query
    await query.answer()
    
    service_key = query.data.split('_')[1]
    context.user_data['service'] = service_key
    context.user_data['service_name'] = REPAIR_SERVICES[service_key]['name']
    context.user_data['price'] = REPAIR_SERVICES[service_key]['price']
    
    await query.edit_message_text(
        f"✅ Selected: {REPAIR_SERVICES[service_key]['name']}\n\n"
        "📱 Enter your phone number:"
    )
    return ENTERING_PHONE

async def phone_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get phone number"""
    phone = update.message.text
    
    context.user_data['phone'] = phone
    await update.message.reply_text(
        "✅ Thank you!\n\n"
        "📱 Enter your device model (e.g., iPhone 12, Samsung Galaxy A51):"
    )
    return ENTERING_DEVICE

async def device_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get device model"""
    device = update.message.text
    context.user_data['device'] = device
    
    await update.message.reply_text(
        "✅ Got it!\n\n"
        "🔍 Describe the problem (max 200 characters):"
    )
    return ENTERING_PROBLEM

async def problem_entered(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get problem description"""
    problem = update.message.text
    if len(problem) > 200:
        await update.message.reply_text("❌ Description too long. Max 200 characters:")
        return ENTERING_PROBLEM
    
    context.user_data['problem'] = problem
    
    # Show order confirmation
    order_summary = f"""📋 **Order Confirmation:**

🔧 Service: {context.user_data['service_name']}
💰 Price: {context.user_data['price']} RUB
📱 Phone: {context.user_data['phone']}
📱 Device: {context.user_data['device']}
🔍 Problem: {context.user_data['problem']}

✅ Is everything correct?
    """
    
    keyboard = [
        [InlineKeyboardButton("✅ Confirm", callback_data="confirm_yes"),
         InlineKeyboardButton("❌ Cancel", callback_data="confirm_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(order_summary, reply_markup=reply_markup, parse_mode='Markdown')
    return CONFIRMING_ORDER

async def order_confirmed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Confirm and save order"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "confirm_no":
        await query.edit_message_text("❌ Order cancelled.")
        return ConversationHandler.END
    
    # Create order
    user_id = update.effective_user.id
    order_id = f"ORD-{user_id}-{len(orders_db) + 1}"
    
    order = {
        'order_id': order_id,
        'user_id': user_id,
        'user_name': update.effective_user.first_name,
        'phone': context.user_data['phone'],
        'device': context.user_data['device'],
        'problem': context.user_data['problem'],
        'service': context.user_data['service_name'],
        'price': context.user_data['price'],
        'status': 'Received',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    orders_db[order_id] = order
    
    confirmation_message = f"""✅ **Order Created Successfully!**

🎟️ Order Number: `{order_id}`
💰 Total: {order['price']} RUB
📍 Status: {order['status']}

⏱️ Expected response time: 30-60 minutes
📍 Address: 123 Main St, Office 205

Thank you for using our service! 🙏
    """
    
    await query.edit_message_text(confirmation_message, parse_mode='Markdown')
    
    return ConversationHandler.END

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's orders"""
    user_id = update.effective_user.id
    user_orders = [order for order in orders_db.values() if order['user_id'] == user_id]
    
    if not user_orders:
        await update.message.reply_text("📭 You have no orders yet")
        return
    
    message = "📋 **Your Orders:**\n\n"
    for order in user_orders:
        message += f"""{order['order_id']}
📱 Device: {order['device']}
🔧 Service: {order['service']}
📊 Status: {order['status']}
⏰ Date: {order['created_at']}
───────────────────
"""
    
    await update.message.reply_text(message, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    text = update.message.text
    
    if text == "📋 New Repair Order":
        return await new_order(update, context)
    elif text == "📊 My Orders":
        await my_orders(update, context)
    elif text == "❓ Help":
        await help_command(update, context)
    elif text == "📞 Contact":
        await contact_command(update, context)
    else:
        await update.message.reply_text("❓ Unknown command. Use menu buttons or /help")

def main():
    """Main function"""
    app = Application.builder().token(TOKEN).build()
    
    # Dialog handler for orders
    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📋 New Repair Order$"), new_order)],
        states={
            CHOOSING_SERVICE: [CallbackQueryHandler(service_chosen)],
            ENTERING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone_entered)],
            ENTERING_DEVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, device_entered)],
            ENTERING_PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, problem_entered)],
            CONFIRMING_ORDER: [CallbackQueryHandler(order_confirmed)]
        },
        fallbacks=[CommandHandler('start', start)]
    )
    
    # Register handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('services', services_command))
    app.add_handler(CommandHandler('contact', contact_command))
    app.add_handler(conversation_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run bot
    print("🤖 Bot started...")
    app.run_polling()

if __name__ == '__main__':
    main()