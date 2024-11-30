# 🌍 Telegram IP Geolocation Bot

[![CodeFactor](https://www.codefactor.io/repository/github/cyberscopetoday/telegram_bot_ip/badge)](https://www.codefactor.io/repository/github/cyberscopetoday/telegram_bot_ip)

This is a simple Telegram bot that provides geolocation information for IP addresses. The bot supports multiple languages, including English, Russian, and Slovak.

## ✨ Features

- 🌐 Language selection support for English, Russian, and Slovak.
- 📍 Provides detailed geolocation information for a given IP address.
- 🛰️ Uses [ip-api.com](http://ip-api.com) to retrieve geolocation data.
- 🗺️ Displays information such as country, region, city, postal code, latitude, longitude, ASN, and organization.

## 📋 Prerequisites

- 🐍 Python 3.7 or higher
- 🤖 [python-telegram-bot](https://python-telegram-bot.readthedocs.io/) library (version 20.0 or higher)
- 🌐 Requests library for making HTTP requests

## 🚀 Installation

1. 📥 Clone the repository:
   ```
   git clone https://github.com/CyberScopeToday/telegram_bot_ip.git
   cd telegram_bot_ip
   ```

2. 🐳 Create a virtual environment:
   ```
   python -m venv venv
   ```

3. 🔄 Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. 📦 Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```

5. 🔑 Replace `'api key bot father'` with your own Telegram bot token, which you can obtain from [BotFather](https://t.me/BotFather).

## 📜 Requirements

Add the following to `requirements.txt`:
```
python-telegram-bot>=20.0
requests
```

## 📚 Usage

1. ▶️ Start the bot by running:
   ```
   python bot_ip-.py
   ```

2. 🤖 Start a conversation with your bot in Telegram by typing `/start`.

3. 🌍 Select your preferred language (English, Russian, or Slovak).

4. 📨 Send an IP address to the bot, and it will provide geolocation information.

## 🛠️ Code Overview

The bot consists of the following main components:

- **🌐 Language Selection**: Users can select their preferred language when they start the bot.
- **📍 Geolocation Retrieval**: When a user sends an IP address, the bot retrieves geolocation data from [ip-api.com](http://ip-api.com).
- **📝 Command Handlers**: Handlers are used to manage user interactions and to process messages.

## 💡 Example

After starting the bot and selecting your language, send an IP address like `8.8.8.8`. The bot will respond with geolocation information, such as:

```
Country: United States
Region: California
City: Mountain View
Postal Code: 94035
Latitude: 37.386
Longitude: -122.0838
ASN: AS15169
Organization: Google LLC
```

## 📝 Logging

The bot uses Python's built-in logging library to log important events, such as user interactions and errors.

## 🤝 Contribution

Feel free to contribute by submitting issues or pull requests. Please make sure to follow the existing code style and include relevant tests where applicable.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This bot uses third-party services (ip-api.com) for geolocation data. Please review their terms of use before using the bot for commercial purposes.
