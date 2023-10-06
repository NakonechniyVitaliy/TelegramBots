from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.web_app_info import WebAppInfo
import json
import config

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://vitaliinakonechniy.pythonanywhere.com/catalog/index_telegram_bot')))
    await message.answer('Вас приветсвует бот SoskaVapeShop!', reply_markup=markup)


@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    res = json.loads(message.web_app_data.data)
    await message.answer(f'Name: {res["name"]} \nEmail: {res["email"]} \nPhone: {res["phone"]} \nProduct: {res["product"]}\nPrice: {res["price"]}')
    int_price = int(res["price"][0:-2])
    await bot.send_invoice(message.chat.id, 'Покупка товарy', res["product"], 'invoice',
                           config.PAYMENT_TOKEN, 'UAH', [types.LabeledPrice('Покупка товара', int_price*100)])


@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def succes(message: types.Message):
    await message.answer(f'Succes: {message.successful_payment.order_info}')


executor.start_polling(dp)
