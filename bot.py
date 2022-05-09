import telebot
from telebot import types



ticker = ''

bot = telebot.TeleBot("5206070667:AAFxwWQPn9DAkkHBZZh3dfZZ5g9vVn2J4ag")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == "Привет":
        bot.reply_to(message, 'Привет от Лори')
    elif message.text == "/ticker":
        bot.send_message(message.from_user.id, "Введите тикер компании")
        bot.register_next_step_handler(message, reg_ticker)
    # bot.reply_to(message, message.text)


def reg_ticker(message):
    global ticker
    ticker = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_multi = types.InlineKeyboardButton(text="Мультипликатор", callback_data='multiplied')
    keyboard.add(key_multi)
    key_comparison = types.InlineKeyboardButton(text="Сравнение", callback_data='comparison')
    keyboard.add(key_comparison)
    question = "Что ты хочешь получить? Мультипликаторы компании " \
               "или сравнение текущей стоимости с годовым минимумом и максимумом?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "multiplied":
        bot.send_message(call.message.chat.id, "Тут будут нужные мультипликаторы")
    elif call.data == "comparison":
        bot.send_message(call.message.chat.id, "Тут будет сравнение стоимости акции")
    bot.send_message(call.message.chat.id, "Введите тикер компании")
    bot.register_next_step_handler(call.message, reg_ticker)


bot.infinity_polling()
