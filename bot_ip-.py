import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

TOKEN = " api tegegram "

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def send_language_selection(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="language:en"),
            InlineKeyboardButton("Русский", callback_data="language:ru"),
            InlineKeyboardButton("Slovenčina", callback_data="language:sk"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose your language / Пожалуйста, выберите ваш язык / Prosím, vyberte váš jazyk:", reply_markup=reply_markup)

def language_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    language = query.data.split(':')[1]
    context.user_data["language"] = language

    if language == "en":
        text = "You have selected English. Now, please send me an IP address to get the geolocation information."
    elif language == "ru":
        text = "Вы выбрали русский язык. Теперь отправьте мне IP-адрес, чтобы получить информацию о геолокации."
    elif language == "sk":
        text = "Vybrali ste slovenčinu. Teraz mi pošlite IP adresu a získate informácie o geolokácii."
    query.edit_message_text(text=text)

def get_geolocation(ip: str, language: str) -> str:
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        print(response.json())

        data = response.json()

        if data["status"] == "success":
            country = data.get("country", "Unknown")
            region = data.get("regionName", "Unknown")
            city = data.get("city", "Unknown")
            postal = data.get("zip", "Unknown")
            lat = data.get("lat", "Unknown")
            lon = data.get("lon", "Unknown")
            asn = data.get("as", "Unknown")
            org = data.get("org", "Unknown")

            if language == "en":
                result = (
                    f"Country: {country}\n"
                    f"Region: {region}\n"
                    f"City: {city}\n"
                    f"Postal Code: {postal}\n"
                    f"Latitude: {lat}\n"
                    f"Longitude: {lon}\n"
                    f"ASN: {asn}\n"
                    f"Organization: {org}\n\n"
                    f"BGP Link: https://bgp.he.net/ip/{ip}\n\n"
                    f"By @mmmurz & @GeoIPInfo_bot"
                )
            elif language == "ru":
                result = (
                    f"Страна: {country}\n"
                    f"Регион: {region}\n"
                    f"Город: {city}\n"
                    f"Город: {city}\n"
                    f"Почтовый индекс: {postal}\n"
                    f"Широта: {lat}\n"
                    f"Долгота: {lon}\n"
                    f"ASN: {asn}\n"
                    f"Организация: {org}\n\n"
                    f"BGP Ссылка: https://bgp.he.net/ip/{ip}\n\n"
                    f"От @mmmurz & @GeoIPInfo_bot"
                )
            elif language == "sk":
                result = (
                    f"Krajina: {country}\n"
                    f"Región: {region}\n"
                    f"Mesto: {city}\n"
                    f"PSČ: {postal}\n"
                    f"Zemepisná šírka: {lat}\n"
                    f"Zemepisná dĺžka: {lon}\n"
                    f"ASN: {asn}\n"
                    f"Organizácia: {org}\n\n"
                    f"BGP Odkaz: https://bgp.he.net/ip/{ip}\n\n"
                    f"Od @mmmurz & @GeoIPInfo_bot"
                )
        else:
            if language == "en":
                result = "Invalid IP address or unable to retrieve geolocation data."
            elif language == "ru":
                result = "Неверный IP-адрес или невозможно получить данные о геолокации."
            elif language == "sk":
                result = "Neplatná IP adresa alebo nie je možné získať údaje o geolokácii."

    except Exception as e:
        logger.error(f"Error while getting geolocation data: {e}")
        if language == "en":
            result = "An error occurred while getting geolocation data."
        elif language == "ru":
            result = "Произошла ошибка при получении данных о геолокации."
        elif language == "sk":
            result = "Pri získavaní údajov o geolokácii sa vyskytla chyba."

    return result

def ip_input(update: Update, context: CallbackContext) -> None:
    ip = update.message.text
    language = context.user_data.get("language", "en")
    result = get_geolocation(ip, language)
    update.message.reply_text(result)

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", send_language_selection))
    dispatcher.add_handler(CallbackQueryHandler(language_callback, pattern="^language:"))
    dispatcher.add_handler(MessageHandler(Filters.regex("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"), ip_input))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
