# Phone Repair Service Telegram Bot

A fully-featured Telegram bot for managing phone repair services with order management, service selection, and order tracking capabilities.

## Features

- **Service Selection**: Users can choose from 7 different repair services
  - 🔋 Battery Replacement (1500 RUB)
  - 📱 Screen Repair (3000 RUB)
  - ⚡ Charging Port Repair (1200 RUB)
  - 🔊 Speaker Repair (800 RUB)
  - 🔘 Button Repair (500 RUB)
  - 💧 Water Damage Service (2000 RUB)
  - 🔧 Other Services

- **Order Management**:
  - Create new repair orders
  - View order history
  - Order confirmation with automatic ID generation
  - Order status tracking

- **User-Friendly Interface**:
  - Interactive inline keyboards for service selection
  - Intuitive menu buttons for easy navigation
  - Multi-step conversation flow for order creation
  - Emoji-rich messages for better UX

- **Commands**:
  - `/start` - Welcome message and menu
  - `/help` - Detailed help and instructions
  - `/services` - List all available services
  - `/contact` - Contact information
  - `/orders` - View your orders

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- A Telegram bot token from @BotFather

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/phone-repair-bot.git
cd phone-repair-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

4. Run the bot:
```bash
python main.py
```

## Usage

1. Start the bot by sending `/start` in Telegram
2. Press "📋 New Repair Order" to create a new order
3. Select a service type
4. Enter your phone number
5. Enter your device model
6. Describe the problem
7. Review and confirm the order
8. Receive your order ID

## Project Structure

```
phone-repair-bot/
├── main.py              # Main bot application
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## Technical Details

### Technologies Used
- **python-telegram-bot** (20.3) - Telegram Bot API wrapper
- **python-dotenv** (1.0.0) - Environment variable management

### Bot Architecture
- Uses `ConversationHandler` for managing multi-step order flow
- Implements inline buttons for service selection
- Stores orders in memory (can be extended to use a database)
- Generates unique order IDs for tracking

## Customization

### Adding New Services
Edit the `REPAIR_SERVICES` dictionary in `main.py`:

```python
REPAIR_SERVICES = {
    'new_service': {'name': '🔧 Service Name', 'price': 1000},
    ...
}
```

### Changing Prices
Update the `price` values in the `REPAIR_SERVICES` dictionary.

### Contact Information
Modify the `contact_command()` function to update contact details.

## Database Integration

Currently, orders are stored in memory. To persist data, you can:
- Use SQLite
- Connect to MongoDB
- Use Firebase
- Implement file-based storage (JSON/CSV)

## Future Enhancements

- Database integration for persistent storage
- Admin panel for managing orders
- Payment integration
- Order notifications
- Multi-language support
- User authentication
- Real-time order status updates

## Troubleshooting

### Bot doesn't respond
- Verify your bot token in `.env`
- Ensure the bot has internet connection
- Check that python-telegram-bot is installed

### Orders not saving
- Currently stored in memory only
- Restart will clear all orders
- Implement database for persistence

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: support@phone-repair.ru
- Phone: +7 (999) 123-45-67

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Author

Created with ❤️ for phone repair businesses
