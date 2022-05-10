import telebot
from telebot import types
import json
from configparser import ConfigParser

# Подключаемся к боту через токен
config = ConfigParser()
config.read_file(open('config.ini'))
bot = telebot.TeleBot(config['Telegram']['token'])


# Начинаем диалог с пользователем
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "Введите название компании")
    bot.register_next_step_handler(message, reg_company)

# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
#     if message.text == "/start":
#         bot.send_message(message.from_user.id, "Введите название компании")
#         bot.register_next_step_handler(message, reg_company)


# Создаем переменную, куда будем сохранять компанию, которую введет пользователь
name_company = ''


# Даем пользователю возможность выбрать, что он хочет получить - Мультипликаторы или стоимость
def reg_company(message):
    global name_company
    name_company = message.text
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
    with open("company_ru.json") as file:
        ru_company = json.load(file)
    with open("company_ru.json") as file:
        ru_company = json.load(file)
    with open("company_usa.json") as file:
        usa_company = json.load(file)
    with open("company_usa.json") as file:
        usa_company = json.load(file)
    if call.data == "multiplied":
        if name_company in ru_company:
            bot.send_message(call.message.chat.id, f"Див доходность: {ru_company.get(name_company)[0]}")
            bot.send_message(call.message.chat.id, f"Дивиденд: {ru_company.get(name_company)[1]}")
            bot.send_message(call.message.chat.id, f"P/S: {ru_company.get(name_company)[2]}")
            bot.send_message(call.message.chat.id, f"P/BV: {ru_company.get(name_company)[3]}")
            bot.send_message(call.message.chat.id, f"P/E: {ru_company.get(name_company)[4]}")
            bot.send_message(call.message.chat.id, f"EV/EBITDA: {ru_company.get(name_company)[5]}")
            bot.send_message(call.message.chat.id, f"Долг/EBITDA: {ru_company.get(name_company)[6]}")
            bot.send_message(call.message.chat.id, f"ROE%: {ru_company.get(name_company)[7]}")
            bot.send_message(call.message.chat.id, f"ROA%: {ru_company.get(name_company)[8]}")
        elif name_company in usa_company:
            bot.send_message(call.message.chat.id, f"Див доходность: {usa_company.get(name_company)[0]}")
            bot.send_message(call.message.chat.id, f"Дивиденд: {usa_company.get(name_company)[1]}")
            bot.send_message(call.message.chat.id, f"P/S: {usa_company.get(name_company)[2]}")
            bot.send_message(call.message.chat.id, f"P/BV: {usa_company.get(name_company)[3]}")
            bot.send_message(call.message.chat.id, f"P/E: {usa_company.get(name_company)[4]}")
            bot.send_message(call.message.chat.id, f"EV/EBITDA: {usa_company.get(name_company)[5]}")
            bot.send_message(call.message.chat.id, f"Долг/EBITDA: {usa_company.get(name_company)[6]}")
            bot.send_message(call.message.chat.id, f"ROE%: {usa_company.get(name_company)[7]}")
            bot.send_message(call.message.chat.id, f"ROA%: {usa_company.get(name_company)[8]}")
        elif name_company not in ru_company or name_company not in usa_company:
            bot.send_message(call.message.chat.id, f"Такой компании нет в списке")
    elif call.data == "comparison":
        bot.send_message(call.message.chat.id, "Тут будет сравнение стоимости акции")
    # bot.send_message(call.message.chat.id, "Введите тикер компании")
    # bot.register_next_step_handler(call.message, reg_ticker)


bot.infinity_polling()
