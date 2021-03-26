import telebot
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config


bot = telebot.TeleBot("TOKEN")


# Greeting
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Привіт, користувачу! Я - ПогодаБот, твій'
                          '\nособистий помічник, що допоможе тобі дізнатися'
                          '\nпогоду у будь якому куточку світу.')


# Sending the weather
@bot.message_handler(content_types=['text'])
def send_info(message):
    config_dict = get_default_config()
    config_dict['language'] = 'ua'  # your language here, eg. Ukrainian
    owm = OWM('KEY', config_dict)
    mgr = owm.weather_manager()

    observation = mgr.weather_at_place(message.text)
    w = observation.weather

    # Temp
    temp = w.temperature('celsius')
    temp_current = temp['temp']
    temp_min = temp['temp_min']
    temp_max = temp['temp_max']
    feels_like = temp['feels_like']

    # Wind
    wind_info = observation.weather.wind(unit='meters_sec')
    wind_speed = wind_info['speed']
    wind_deg = wind_info['deg']

    bot.reply_to(message, 'Температура зараз: ' + str(temp_current) +
                          '\n  \nМінімальна температура сьогодні: ' +
                          str(temp_min) + ' градуси'
                          '\n \nМаксимальна температура сьогодні: ' +
                          str(temp_max) + ' градуси' +
                          '\n \nВідчувається як: ' + str(feels_like) +
                          ' градуси' + '\n \nШвидкість вітру' +
                          'сьогодні: ' +
                          str(wind_speed) + ' метра за секунду' +
                          '\n \n Напрям вітру у градусах від ' +
                          'північного ' + 'горизонту:  ' + str(wind_deg))


bot.polling()
