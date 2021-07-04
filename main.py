import config
import telebot
import requests

from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot(config.Token)

link_short = "https://yandex.ru/pogoda/moscow"

check = requests.get(link_short).text

soup = BeautifulSoup(check, 'lxml')

block = soup.find('div', class_='forecast-briefly__days')
test = block.find('ul', class_='swiper-wrapper')


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

                day = test.find_all('div')[7].text[4:]
                night = test.find_all('div')[8].text[5:]
                status = test.find_all('div')[9].text

                result = f'Температура днем: {day}\nТемпература ночью: {night}\n{status}'

                bot.send_message(call.message.chat.id, result)
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Кратко',
                                      reply_markup=None)

            elif call.data == 'Yes_Tomorrow':
                day = test.find_all('div')[12].text[4:]
                night = test.find_all('div')[13].text[5:]
                status = test.find_all('div')[14].text

                result = f'Температура днем: {day}\nТемпература ночью: {night}\n{status}'

                bot.send_message(call.message.chat.id, result)
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Кратко',
                                      reply_markup=None)

            elif call.data == 'Yes_Week':

                day = test.find_all('div')[7].text[4:]
                night = test.find_all('div')[8].text[5:]
                status = test.find_all('div')[9].text

                day1 = test.find_all('div')[12].text[4:]
                night1 = test.find_all('div')[13].text[5:]
                status1 = test.find_all('div')[14].text

                name2 = test.find_all('div')[16].text
                day2 = test.find_all('div')[17].text[4:]
                night2 = test.find_all('div')[18].text[5:]
                status2 = test.find_all('div')[19].text

                name3 = test.find_all('div')[21].text
                day3 = test.find_all('div')[22].text[4:]
                night3 = test.find_all('div')[23].text[5:]
                status3 = test.find_all('div')[24].text

                name4 = test.find_all('div')[26].text
                day4 = test.find_all('div')[27].text[4:]
                night4 = test.find_all('div')[28].text[5:]
                status4 = test.find_all('div')[29].text

                name5 = test.find_all('div')[31].text
                day5 = test.find_all('div')[32].text[4:]
                night5 = test.find_all('div')[33].text[5:]
                status5 = test.find_all('div')[34].text

                name6 = test.find_all('div')[36].text
                day6 = test.find_all('div')[37].text[4:]
                night6 = test.find_all('div')[38].text[5:]
                status6 = test.find_all('div')[39].text

                result = f'Сегодня:\nПогода днем:{day}\nПогода вечером:{night}\n{status}\n' \
                         f'Завтра:\nПогода днем:{day1}\nПогода вечером:{night1}\n{status1}\n' \
                         f'{name2}:\nПогода днем:{day2}\nПогода вечером:{night2}\n{status2}\n' \
                         f'{name3}:\nПогода днем:{day3}\nПогода вечером:{night3}\n{status3}\n' \
                         f'{name4}:\nПогода днем:{day4}\nПогода вечером:{night4}\n{status4}\n' \
                         f'{name5}:\nПогода днем:{day5}\nПогода вечером:{night5}\n{status5}\n' \
                         f'{name6}:\nПогода днем:{day6}\nПогода вечером:{night6}\n{status6}\n'

                bot.send_message(call.message.chat.id, result)
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Кратко',
                                      reply_markup=None)

            elif call.data == 'No_Today':
                bot.send_message(call.message.chat.id, 'Кек1')
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Подробно',
                                      reply_markup=None)

            elif call.data == 'No_Tomorrow':
                bot.send_message(call.message.chat.id, 'Кек2')
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Подробно',
                                      reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
