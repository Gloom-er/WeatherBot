import config
import telebot
import requests

from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot(config.Token)

link_short = "https://yandex.ru/pogoda/moscow"

check = requests.get(link_short).text

soup = BeautifulSoup(check, 'lxml')

block_day = soup.find('div', class_="temp forecast-briefly__temp forecast-briefly__temp_day")
day = block_day.find_all('span')[1].text
block_night = soup.find('div', class_="temp forecast-briefly__temp forecast-briefly__temp_night")
night = block_night.find_all('span')[1].text
status = soup.find('div', class_="forecast-briefly__condition").text
result = f'Температура днем: {day}\nТемпература ночью: {night}\n{status}'


@bot.message_handler(commands=['start'])
def welcome(message):
    sticker = open('Кир.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton("Сегодня")
    button2 = types.KeyboardButton("Завтра")
    button3 = types.KeyboardButton("Вся неделя")

    markup.add(button1, button2, button3)

    bot.send_message(message.chat.id,
                     "Приветствую, {0.first_name}!\nЯ - {1.first_name}, бот, который расскажет все о погоде.".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.chat.type == 'private':
        if message.text == 'Сегодня':

            markup = types.InlineKeyboardMarkup(row_width=2)
            question1 = types.InlineKeyboardButton("Да", callback_data='Yes_Today')
            question2 = types.InlineKeyboardButton("Нет", callback_data='No_Today')

            markup.add(question1, question2)

            bot.send_message(message.chat.id, str("Кратко?"), reply_markup=markup)

        elif message.text == 'Завтра':

            markup = types.InlineKeyboardMarkup(row_width=2)
            question1 = types.InlineKeyboardButton("Да", callback_data='Yes_Tomorrow')
            question2 = types.InlineKeyboardButton("Нет", callback_data='No_Tomorrow')

            markup.add(question1, question2)

            bot.send_message(message.chat.id, str("Кратко?"), reply_markup=markup)

        elif message.text == 'Вся неделя':

            markup = types.InlineKeyboardMarkup(row_width=2)
            question1 = types.InlineKeyboardButton("Да", callback_data='Yes_Week')
            question2 = types.InlineKeyboardButton("Нет", callback_data='No_Week')

            markup.add(question1, question2)

            bot.send_message(message.chat.id, str("Кратко?"), reply_markup=markup)
        else:
            bot.send_message(message.chat.id, str("Такого ответа нет"))


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        if call.message:
            if call.data == 'Yes_Today':
                bot.send_message(call.message.chat.id, result)

                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Кратко',
                                      reply_markup=None)
            elif call.data == 'No_Today':
                bot.send_message(call.message.chat.id, 'Кек1')

                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Подробно',
                                      reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
