import telebot
from telebot import types
import requests
import currency  # Currency parser

bot_token = open("BOT_ACCESS").read()
bot = telebot.TeleBot(bot_token)

currency_list = {"CAD": "Канадский доллар",
                 "HKD": "Гонконгский доллар",
                 "ISK": "Исландская крона",
                 "PHP": "Филлипинское песо",
                 "DKK": "Датская крона",
                 "HUF": "Венгерский форинт",
                 "CZK": "Чешская крона",
                 "GBP": "Фунт стерлингов",
                 "RON": "Румынский лей",
                 "SEK": "Шведская крона",
                 "IDR": "Индонезийская рупия",
                 "INR": "Индийская рупия",
                 "BRL": "Бразильский реал",
                 "RUB": "Российский рубль",
                 "HRK": "Хорватская куна",
                 "JPY": "Японская иена",
                 "THB": "Тайский бат",
                 "CHF": "Швейцарсикй франк",
                 "EUR": "Евро",
                 "MYR": "Малайзийский ринггит",
                 "BGN": "Болгарский лев",
                 "TRY": "Турецкая лира",
                 "CNY": "Китайский юань",
                 "NOK": "Норвежская крона",
                 "NZD": "Новозеландский доллар",
                 "ZAR": "Южноафриканский рэнд",
                 "USD": "Доллар США",
                 "MXN": "Мексиканское песо",
                 "SGD": "Сингапурский доллар",
                 "AUD": "Австралийский доллар",
                 "ILS": "Новый израильский шекель",
                 "KRW": "Южнокорейская вона",
                 "PLN": "Польский злотый"
                 }
currency_listR = {v: k for k, v in currency_list.items()}

inlineMarkup = types.InlineKeyboardMarkup()
for x in currency_listR:
    button = types.InlineKeyboardButton(text=str(x + " " + currency_listR[x]), callback_data=str(currency_listR[x]))
    inlineMarkup.add(button)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
EUR = types.KeyboardButton("EUR💶")
USD = types.KeyboardButton("USD💵")
own = types.KeyboardButton("Полный список")
markup.add(EUR, USD, own)

messageID = int()


@bot.message_handler(commands=['start'])
def sendMessage(message):
    global messageID
    messageID = message.chat.id
    if message.chat.id == 295794680:
        bot.send_message(message.chat.id, "Здравствуй, создатель")
    else:
        bot.send_message(message.chat.id, "Привет, <b>{0.first_name}</b>!".format(message.from_user, bot.get_me),
                         parse_mode='html')
    bot.send_message(message.chat.id, "Я могу прислать тебе актуальный курс валют!", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def answer(message):
    global messageID
    messageID = message.chat.id
    if message.text == "EUR💶":
        bot.send_message(message.chat.id, currency.EUR(), reply_markup=markup)
    elif message.text == "USD💵":
        bot.send_message(message.chat.id, currency.USD(), reply_markup=markup)
    elif message.text == "Полный список":
        bot.send_message(message.chat.id, "Выберите интересующую вас валюту", reply_markup=inlineMarkup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.send_message(messageID, currency.own(currency_list[call.data], call.data))
    telebot.TeleBot.answer_callback_query(bot, call.id)


bot.polling(none_stop=True)
