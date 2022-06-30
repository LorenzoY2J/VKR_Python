import json
from configparser import ConfigParser
import telebot
from telebot import types
import parcing_price_ru
import parcing_ru

# Подключаемся к боту через токен
config = ConfigParser()
config.read_file(open('config.ini'))
bot = telebot.TeleBot(config['Telegram']['token'])


# Начинаем диалог с пользователем
@bot.message_handler(commands=['start'])
def send_welcome(message):
    ticker_help = types.InlineKeyboardMarkup()
    ticker_help.add(types.InlineKeyboardButton("Все компании мосбиржи",
                                               url='https://finsovetnik.com/rf/'))
    bot.send_message(message.from_user.id, f"Привет, <b>{message.from_user.first_name}</b>! "
                                           f"Введите тикер интересующей компании."
                     , parse_mode='html', reply_markup=ticker_help)
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
    key_multi = types.InlineKeyboardButton(text="Мультипликаторы", callback_data='multiplied')
    keyboard.add(key_multi)
    key_comparison = types.InlineKeyboardButton(text="Стоимость акции", callback_data='comparison')
    keyboard.add(key_comparison)
    question = "Что ты хочешь получить? Мультипликаторы компании " \
               "или текущую стоимость?"
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "multiplied":
        parcing_ru.parcing_milti()
        with open("company_ru.json") as file:
            ru_company = json.load(file)
        # Тестирование выдачи всех компаний из списка мультипликаторов
        # for i in ru_company:
        #     name_company = i
        if name_company in ru_company:
            multi_help = types.InlineKeyboardMarkup()
            multi_help.add(types.InlineKeyboardButton("Статья о мультипликаторах",
                                                      url='https://telegra.ph/Podrobnee-pro-multiplikatory-06-12'))
            bot.send_message(call.message.chat.id, f"Текущие мультипликаторы компании "
                                                   f"<b>{ru_company.get(name_company)[0]}</b>:\n"
                                                   f"* Див доходность: {ru_company.get(name_company)[1][0]}%\n"
                                                   f"* Дивиденд: {ru_company.get(name_company)[1][1]} рублей\n"
                                                   f"* P/E: {ru_company.get(name_company)[1][4]}\n"
                                                   f"* P/S: {ru_company.get(name_company)[1][2]}\n"
                                                   f"* P/BV: {ru_company.get(name_company)[1][3]}\n"
                                                   f"* EV/EBITDA: {ru_company.get(name_company)[1][5]}\n"
                                                   f"* Долг/EBITDA: {ru_company.get(name_company)[1][6]}\n"
                                                   f"* ROE%: {ru_company.get(name_company)[1][7]}%\n"
                                                   f"* ROA%: {ru_company.get(name_company)[1][8]}%\n",
                             parse_mode='html', reply_markup=multi_help)
        elif name_company not in ru_company:
            ticker_help_2 = types.InlineKeyboardMarkup()
            ticker_help_2.add(types.InlineKeyboardButton("Все компании мосбиржи",
                                                       url='https://finsovetnik.com/rf/'))
            bot.send_message(call.message.chat.id,
                             f"Такой компании нет в списке или вы набрали название компании, а не ее тикер"
                             , reply_markup=ticker_help_2)
    elif call.data == "comparison":
        parcing_price_ru.parcing_price()
        with open("company_price_ru.json") as file:
            ru_price_company = json.load(file)
        # Тестирование выдачи всех компаний из списка стоимости компаний
        # for items in ru_price_company:
        #     name_company = items
        if name_company in ru_price_company:
            bot.send_message(call.message.chat.id, f"Текущая цена акции компании "
                                                   f"<b>{ru_price_company.get(name_company)[1]}</b> = "
                                                   f"{ru_price_company.get(name_company)[0]} рублей", parse_mode='html')
        elif name_company not in ru_price_company:
            ticker_help_3 = types.InlineKeyboardMarkup()
            ticker_help_3.add(types.InlineKeyboardButton("Все компании мосбиржи",
                                                       url='https://finsovetnik.com/rf/'))
            bot.send_message(call.message.chat.id,
                             f"Такой компании нет в списке или вы набрали название компании, а не ее тикер"
                             , reply_markup=ticker_help_3)
    bot.send_message(call.message.chat.id, "Введите тикер компании")
    bot.register_next_step_handler(call.message, reg_company)


if __name__ == '__main__':
    bot.polling(none_stop=True)
