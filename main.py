import config
import telebot
import requests

from bs4 import BeautifulSoup
from telebot import types

bot = telebot.TeleBot(config.Token)

link_short = "https://yandex.ru/pogoda/moscow"
link_long = "https://yandex.ru/pogoda/moscow/details"

check = requests.get(link_short).text
check_long = requests.get(link_long).text

soup = BeautifulSoup(check, 'lxml')
soup_long = BeautifulSoup(check_long, 'lxml')

block = soup.find('div', class_='forecast-briefly__days')
block_long = soup_long.find_all('div', class_='card')

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

                test_long = block_long[0].find('tbody', 'weather-table__body')
                day_long = test_long.find_all('tr')

                temp_Today_morning = day_long[0].find('div', class_='weather-table__temp').text
                status_Today_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_condition').text
                pressure_Today_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                       'weather-table__body-cell_type_air-pressure').text
                wet_Today_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                  'weather-table__body-cell_type_humidity').text
                wind_Today_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                   'weather-table__body-cell_type_wind '
                                                                   'weather-table__body-cell_wrapper').text
                feels_Today_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                    'weather-table__body-cell_type_feels-like').text

                temp_Today_daytime = day_long[1].find('div', class_='weather-table__temp').text
                status_Today_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_condition').text
                pressure_Today_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                       'weather-table__body-cell_type_air-pressure').text
                wet_Today_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                  'weather-table__body-cell_type_humidity').text
                wind_Today_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                   'weather-table__body-cell_type_wind '
                                                                   'weather-table__body-cell_wrapper').text
                feels_Today_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                    'weather-table__body-cell_type_feels-like').text

                temp_Today_evening = day_long[2].find('div', class_='weather-table__temp').text
                status_Today_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_condition').text
                pressure_Today_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                       'weather-table__body-cell_type_air-pressure').text
                wet_Today_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                  'weather-table__body-cell_type_humidity').text
                wind_Today_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                   'weather-table__body-cell_type_wind '
                                                                   'weather-table__body-cell_wrapper').text
                feels_Today_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                    'weather-table__body-cell_type_feels-like').text

                temp_Today_night = day_long[2].find('div', class_='weather-table__temp').text
                status_Today_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                   'weather-table__body-cell_type_condition').text
                pressure_Today_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_air-pressure').text
                wet_Today_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                'weather-table__body-cell_type_humidity').text
                wind_Today_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                 'weather-table__body-cell_type_wind '
                                                                 'weather-table__body-cell_wrapper').text
                feels_Today_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                  'weather-table__body-cell_type_feels-like').text

                result_Today = f'Температура утром:{temp_Today_morning} {status_Today_morning} ' \
                               f'Давление:{pressure_Today_morning} Влажность:' \
                               f'{wet_Today_morning} Ветер:{wind_Today_morning} Ощущается как:{feels_Today_morning}\n' \
                               f'Температура днем:{temp_Today_daytime} {status_Today_daytime} ' \
                               f'Давление:{pressure_Today_daytime} Влажность:' \
                               f'{wet_Today_daytime} Ветер:{wind_Today_daytime} Ощущается как:{feels_Today_daytime}\n' \
                               f'Температура вечером:{temp_Today_evening} {status_Today_evening} ' \
                               f'Давление:{pressure_Today_evening} Влажность:' \
                               f'{wet_Today_evening} Ветер:{wind_Today_evening} Ощущается как:{feels_Today_evening}\n' \
                               f'Температура ночью:{temp_Today_night} {status_Today_night} ' \
                               f'Давление:{pressure_Today_night} Влажность:' \
                               f'{wet_Today_night} Ветер:{wind_Today_night} Ощущается как:{feels_Today_night}'

                bot.send_message(call.message.chat.id, result_Today)
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Подробно',
                                      reply_markup=None)

            elif call.data == 'No_Tomorrow':

                test_long = block_long[2].find('tbody', 'weather-table__body')
                day_long = test_long.find_all('tr')

                temp_Tomorrow_morning = day_long[0].find('div', class_='weather-table__temp').text
                status_Tomorrow_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                        'weather-table__body-cell_type_condition').text
                pressure_Tomorrow_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                          'weather-table__body-cell_type_air-pressure').text
                wet_Tomorrow_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_humidity').text
                wind_Tomorrow_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                      'weather-table__body-cell_type_wind '
                                                                      'weather-table__body-cell_wrapper').text
                feels_Tomorrow_morning = day_long[0].find('td', class_='weather-table__body-cell '
                                                                       'weather-table__body-cell_type_feels-like').text

                temp_Tomorrow_daytime = day_long[1].find('div', class_='weather-table__temp').text
                status_Tomorrow_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                        'weather-table__body-cell_type_condition').text
                pressure_Tomorrow_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                          'weather-table__body-cell_type_air-pressure').text
                wet_Tomorrow_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_humidity').text
                wind_Tomorrow_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                      'weather-table__body-cell_type_wind '
                                                                      'weather-table__body-cell_wrapper').text
                feels_Tomorrow_daytime = day_long[1].find('td', class_='weather-table__body-cell '
                                                                       'weather-table__body-cell_type_feels-like').text

                temp_Tomorrow_evening = day_long[2].find('div', class_='weather-table__temp').text
                status_Tomorrow_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                        'weather-table__body-cell_type_condition').text
                pressure_Tomorrow_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                          'weather-table__body-cell_type_air-pressure').text
                wet_Tomorrow_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_humidity').text
                wind_Tomorrow_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                      'weather-table__body-cell_type_wind '
                                                                      'weather-table__body-cell_wrapper').text
                feels_Tomorrow_evening = day_long[2].find('td', class_='weather-table__body-cell '
                                                                       'weather-table__body-cell_type_feels-like').text

                temp_Tomorrow_night = day_long[2].find('div', class_='weather-table__temp').text
                status_Tomorrow_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                      'weather-table__body-cell_type_condition').text
                pressure_Tomorrow_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                        'weather-table__body-cell_type_air-pressure').text
                wet_Tomorrow_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                   'weather-table__body-cell_type_humidity').text
                wind_Tomorrow_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                    'weather-table__body-cell_type_wind '
                                                                    'weather-table__body-cell_wrapper').text
                feels_Tomorrow_night = day_long[2].find('td', class_='weather-table__body-cell '
                                                                     'weather-table__body-cell_type_feels-like').text

                result_Tomorrow = f'Температура утром:{temp_Tomorrow_morning} {status_Tomorrow_morning} ' \
                                  f'Давление:{pressure_Tomorrow_morning} Влажность:' \
                                  f'{wet_Tomorrow_morning} Ветер:{wind_Tomorrow_morning} Ощущается как:{feels_Tomorrow_morning}\n' \
                                  f'Температура днем:{temp_Tomorrow_daytime} {status_Tomorrow_daytime} ' \
                                  f'Давление:{pressure_Tomorrow_daytime} Влажность:' \
                                  f'{wet_Tomorrow_daytime} Ветер:{wind_Tomorrow_daytime} Ощущается как:{feels_Tomorrow_daytime}\n' \
                                  f'Температура вечером:{temp_Tomorrow_evening} {status_Tomorrow_evening} ' \
                                  f'Давление:{pressure_Tomorrow_evening} Влажность:' \
                                  f'{wet_Tomorrow_evening} Ветер:{wind_Tomorrow_evening} Ощущается как:{feels_Tomorrow_evening}\n' \
                                  f'Температура ночью:{temp_Tomorrow_night} {status_Tomorrow_night} ' \
                                  f'Давление:{pressure_Tomorrow_night} Влажность:' \
                                  f'{wet_Tomorrow_night} Ветер:{wind_Tomorrow_night} Ощущается как:{feels_Tomorrow_night}'

                bot.send_message(call.message.chat.id, result_Tomorrow)
                #   remove inline button
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Подробно',
                                      reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
