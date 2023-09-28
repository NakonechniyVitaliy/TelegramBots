import telebot
import requests
import json
from telebot import types
import pendulum


bot = telebot.TeleBot('6004819473:AAEChj6FYurBInriyyJUPp9T8eIEejNLkxU')
API = 'a8cf8f805d6dd6a06343ef2612485021'

today = pendulum.today('Europe/Kiev').format('MM-DD')
tomorrow = pendulum.tomorrow('Europe/Kiev').format('MM-DD')

city = 'None'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши город в котором хочешь узнать погоду')
    bot.register_next_step_handler(message, town)


def town(message):
    global city
    city = str(message.text.strip())
    res = requests.get(f'https://api.openweathermap.org/data/2.5/forecast/?q={city}&appid={API}&units=metric',
                       params={'lang': 'ru'})
    if res.status_code == 200:
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn0 = types.InlineKeyboardButton('Погода сейчас', callback_data='now')
        btn1 = types.InlineKeyboardButton('Прогноз на сегодня', callback_data='today')
        btn2 = types.InlineKeyboardButton('Прогноз на завтра', callback_data='tomorrow')
        btn3 = types.InlineKeyboardButton('Прогноз на 5 дней', callback_data='week')
        markup.add(btn0, btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Выберите прогноз ☀⛅☁️', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неправильно указаный город, попробуйте ещё раз')
        bot.register_next_step_handler(message, town)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/forecast/?q={city}&appid={API}&units=metric',
                       params={'lang': 'ru'})
    data = json.loads(res.text)
    for i in data['list']:
        forecast = (i['dt_txt'][5:16], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
        forecast = list(forecast)
        if forecast[2] == 'небольшая облачность':
            forecast[2] = 'небольшая облачность 🌤'
        elif forecast[2] == 'ясно':
            forecast[2] = 'ясно ☀️'
        elif forecast[2] == 'облачно с прояснениями':
            forecast[2] = 'облачно с прояснениями ⛅️'
        elif forecast[2] == 'пасмурно':
            forecast[2] = 'пасмурно ☁️'
        elif forecast[2] == 'небольшой дождь':
            forecast[2] = 'небольшой дождь 🌦'
        elif forecast[2] == 'дождь':
            forecast[2] = 'дождь 🌧'
        elif forecast[2] == 'снег':
            forecast[2] = 'снег 🌨'
        elif forecast[2] == 'гроза ':
            forecast[2] = 'гроза ⛈'
        elif forecast[2] == 'переменная облачность':
            forecast[2] = 'переменная облачность 🌥'

        if call.data == 'today':
            if forecast[0][:5] == today:
                if forecast[0][6:] == '03:00' or forecast[0][6:] == '09:00' or \
                        forecast[0][6:] == '15:00' or forecast[0][6:] == '21:00':
                    forecast_message = (f'Время: {forecast[0]} \nТемпература: {forecast[1]}° \nНебо: {forecast[2]}')
                    bot.send_message(call.message.chat.id, forecast_message)

        if call.data == 'tomorrow':
            if forecast[0][:5] == tomorrow:
                if forecast[0][6:] == '03:00' or forecast[0][6:] == '09:00' or \
                        forecast[0][6:] == '15:00' or forecast[0][6:] == '21:00':
                    forecast_message = (f'Время: {forecast[0]} \nТемпература: {forecast[1]}° \nНебо: {forecast[2]}')
                    bot.send_message(call.message.chat.id, forecast_message)

        if call.data == 'week':
            if forecast[0][6:] == '03:00' or forecast[0][6:] == '09:00' or \
                    forecast[0][6:] == '15:00' or forecast[0][6:] == '21:00':
                forecast_message = (f'Время: {forecast[0]} \nТемпература: {forecast[1]}° \nНебо: {forecast[2]}')
                bot.send_message(call.message.chat.id, forecast_message)

    if call.data == 'now':
        res_2 = requests.get(f'https://api.openweathermap.org/data/2.5/weather/?q={city}&appid={API}&units=metric',
                           params={'lang': 'ru'})
        data_2 = json.loads(res_2.text)
        bot.send_message(call.message.chat.id, f"Сейчас: {int(data_2['main']['temp'])}°")
        main = data_2["weather"]
        main_2 = main[0]
        weather = main_2['main']
        if weather == 'Clear':
            bot.send_message(call.message.chat.id, '☀️')
        if weather == 'Clouds':
            bot.send_message(call.message.chat.id, '☁️')
        if weather == 'Rain':
            bot.send_message(call.message.chat.id, '🌧️')
        if weather == 'Snow':
            bot.send_message(call.message.chat.id, '🌨️')

    bot.send_message(call.message.chat.id, 'Можете написать новый город')
    bot.register_next_step_handler(call.message, town)


bot.polling(none_stop=True)
