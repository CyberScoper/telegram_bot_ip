import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = 'API BOTFATHER'  # Замените на ваш реальный токен

# Удаление существующего вебхука
response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook')
print(response.text)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Функция для отправки выбора языка
async def send_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='language:en'),
            InlineKeyboardButton("Русский", callback_data='language:ru'),
            InlineKeyboardButton("Slovenčina", callback_data='language:sk'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Please choose your language / Пожалуйста, выберите ваш язык / Prosím, vyberte váš jazyk:",
        reply_markup=reply_markup
    )
    logger.info(f"User {update.message.from_user.id} ({update.message.from_user.username}) initiated language selection.")

# Обработчик выбора языка
async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    language = query.data.split(':')[1]
    context.user_data["language"] = language
    text = {
        "en": "You have selected English. Now, please send me an IP address to get the geolocation information.",
        "ru": "Вы выбрали русский язык. Теперь отправьте мне IP-адрес, чтобы получить информацию о геолокации.",
        "sk": "Vybrali ste slovenčinu. Teraz mi pošlite IP adresu a získate informácie o geolokácii."
    }.get(language, "Language not supported.")
    await query.edit_message_text(text=text)
    logger.info(f"User {query.from_user.id} ({query.from_user.username}) selected language: {language}.")

# Функция для получения геолокации
def get_geolocation(ip: str, language: str) -> str:
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if data["status"] == "success":
            info = {k: data.get(k, "Unknown") for k in ["country", "regionName", "city", "zip", "lat", "lon", "as", "org"]}
            link = f"https://bgp.he.net/ip/{ip}"
            template = (
                "Country: {country}\nRegion: {regionName}\nCity: {city}\nPostal Code: {zip}\n"
                "Latitude: {lat}\nLongitude: {lon}\nASN: {as}\nOrganization: {org}\n\n"
                "BGP Link: {link}\n\nBy @mmmurz & @GeoIPInfo_bot"
            )
            if language == "ru":
                template = template.replace("Country", "Страна").replace("Region", "Регион") \
                    .replace("City", "Город").replace("Postal Code", "Почтовый индекс") \
                    .replace("Latitude", "Широта").replace("Longitude", "Долгота") \
                    .replace("ASN", "ASN").replace("Organization", "Организация")
            elif language == "sk":
                template = template.replace("Country", "Krajina").replace("Region", "Región") \
                    .replace("City", "Mesto").replace("Postal Code", "PSČ") \
                    .replace("Latitude", "Zemepisná šírka").replace("Longitude", "Zemepisná dĺžka") \
                    .replace("ASN", "ASN").replace("Organization", "Organizácia")
            result = template.format(**info, link=link)
        else:
            result = {
                "en": "Invalid IP address or unable to retrieve geolocation data.",
                "ru": "Неверный IP-адрес или невозможно получить данные о геолокации.",
                "sk": "Neplatná IP adresa alebo nie je možné získať údaje o geolokácii."
            }.get(language, "Language not supported.")
    except Exception as e:
        logger.error(f"Error while getting geolocation data: {e}")
        result = {
            "en": "An error occurred while getting geolocation data.",
            "ru": "Произошла ошибка при получении данных о геолокации.",
            "sk": "Pri získavaní údajov o geolokácii sa vyskytla chyba."
        }.get(language, "An error occurred.")
    return result

# Обработчик ввода IP
async def ip_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ip = update.message.text
    language = context.user_data.get("language", "en")
    result = get_geolocation(ip, language)
    await update.message.reply_text(result)
    logger.info(f"User {update.message.from_user.id} ({update.message.from_user.username}) requested geolocation for IP: {ip}.")

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", send_language_selection))
    application.add_handler(CallbackQueryHandler(language_callback, pattern='^language:'))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ip_input))

    application.run_polling()

if __name__ == '__main__':
    main()
