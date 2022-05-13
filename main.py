# -*- coding: utf-8 -*-
# import modules:
from api import Database, search_profession

# import libraries:
import telebot
from telebot import types

bot = telebot.TeleBot("5333022128:AAEBsg_DAb20lLYh5oA0SdrfGiQO-D8h8Bk")
db = Database('vacancies.db')

listButtonChat = {}
listPathForChat = {'finance': ['accounting', 'management', "Выберите сферу финансов:", 0],
                   'it': ['gamedesigners', 'developers', "Выберите профессию:", 0],
                   'gamedesigners': ['Languages', 1],
                   'developers': ['Languages', 1],
                   'accounting': ['crisisAnalytics', 'registration', "Выберите сферу:", 1],
                   'management': ['state', 'entrepreneurial', "Выберите сферу:", 1],
                   'crisisAnalytics': ['profession', 2],
                   'registration': ['profession', 2],
                   'state': ['profession', 2],
                   'entrepreneurial': ['profession', 2],
                   'languages': ['profession', 2],
                   'district': [3],
                   'Next_vac:': ['Next_vac']
                   }
languages = {'Python': ['G', 'D'], 'C++': ['G', 'D'], 'C#': ['G', 'D'], 'Swift': ['G', 'D'],
             'Java': ['G', 'D'],
             'Assembler': ['G'], 'Rust': ['D'], 'JavaScript': ['D'], 'SQL': ['D'], 'Kotlin': ['D']}
listKeyboardLanguages = {'G': [], 'D': []}
massKeyboardDistrict = []
nameDistricts = ['СЗАО', 'САО', 'СВАО', 'ЗАО', 'ЦАО', 'ВАО', 'ЮЗАО', 'ЮАО', 'ЮВАО']

new_call = 'Next_vac:'
temp_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
    types.InlineKeyboardButton(text='Показать следующие вакансии', callback_data=new_call))

checkStatus = {}

vacancies = {}


@bot.message_handler(commands=["start"])
def start(message):
    text_hello = 'Доброго времени суток! Я бот для поиска работы, ' \
                 'созданный специально для помощи в этом молодым ' \
                 'специалистам в городе Москва.'
    bot.send_message(message.chat.id, text_hello)

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(listButtonChat['finance'], listButtonChat['it'])
    checkStatus[message.chat.id] = [None] * 4
    bot.send_message(message.chat.id,
                     "Напишите команду /feedback для того, чтобы сообщить нам о проблемах " \
                     "и доработках.",
                     reply_markup=markup_inline)


@bot.message_handler(commands=["feedback"])
def feedback(message):
    text_hello = 'Ваши вопросы и пожелания просьба направлять на нашу почту: ' \
                 'tgbotsearchforjob@gmail.com.'
    bot.send_message(message.chat.id, text_hello)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data in list(languages.keys()):
        value = listPathForChat['languages']
    elif call.data in nameDistricts:
        value = listPathForChat['district']
    else:
        value = listPathForChat[call.data]

    if value[0] == 'Next_vac':
        page = vacancies[call.message.chat.id][1]
        array = vacancies[call.message.chat.id][0]

        len_of_array = len(array)
        len_for_vacancies = 0
        need_keyboard = False

        if len_of_array - (page * 5) > 5:
            need_keyboard = True
            len_for_vacancies = (page * 5) + 5
        else:
            len_for_vacancies = len_of_array

        print_vacancy(call.message.chat.id, (page * 5), len_for_vacancies)

        if need_keyboard:
            array = vacancies[call.message.chat.id][0]
            page = vacancies[call.message.chat.id][1] + 1
            vacancies[call.message.chat.id] = [array, page]

            bot.send_message(call.message.chat.id, 'Вы желаете просмотреть ещё вакансии?',
                             reply_markup=temp_keyboard)
        else:
            bot.send_message(call.message.chat.id, 'На данный момент это все вакансии.')
    elif type(value[0]) == int:
        index = value[0]
        checkStatus[call.message.chat.id][index] = call.data

        profession = checkStatus[call.message.chat.id][0]
        table = checkStatus[call.message.chat.id][1]
        specialization = checkStatus[call.message.chat.id][2]
        district = checkStatus[call.message.chat.id][3]

        bot.send_message(call.message.chat.id, 'Подождите немного, происходит поиск вакансий по заданным критериям.')

        search_profession(call.message.chat.id, db, table, profession, specialization, district)
        vacancies[call.message.chat.id] = [db.read(call.message.chat.id, table).copy(), 0]

        len_of_array = len(vacancies[call.message.chat.id][0])
        len_for_vacancies = 0
        need_keyboard = False

        if len_of_array > 5:
            len_for_vacancies = 5
            need_keyboard = True
        else:
            len_for_vacancies = len_of_array

        print_vacancy(call.message.chat.id, 0, len_for_vacancies)

        if need_keyboard:
            array = vacancies[call.message.chat.id][0]
            page = vacancies[call.message.chat.id][1] + 1
            vacancies[call.message.chat.id] = [array, page]

            bot.send_message(call.message.chat.id, 'Вы желаете просмотреть ещё вакансии?',
                             reply_markup=temp_keyboard)
        else:
            if len_for_vacancies == 0:
                bot.send_message(call.message.chat.id, 'По заданным критериям вакансии отсутствуют.')
            else:
                bot.send_message(call.message.chat.id, 'На данный момент это все вакансии.')
    elif value[0] == 'profession':
        index = value[1]
        checkStatus[call.message.chat.id][index] = call.data
        markup_inline_district = types.InlineKeyboardMarkup()
        for i in range(0, len(massKeyboardDistrict), 3):
            try:
                markup_inline_district.add(massKeyboardDistrict[i], massKeyboardDistrict[i + 1],
                                           massKeyboardDistrict[i + 2])
            except Exception as err:
                pass
        bot.send_message(call.message.chat.id, "Выберите округ:",
                         reply_markup=markup_inline_district)
    elif value[0] == 'Languages':
        markup_inline_languages = types.InlineKeyboardMarkup()
        buttons = listKeyboardLanguages['G' if call.data == 'gameDesign' else 'D']
        for i in range(0, len(buttons), 3):
            try:
                markup_inline_languages.add(buttons[i], buttons[i + 1], buttons[i + 2])
            except Exception as err:
                pass
        bot.send_message(call.message.chat.id, "Выберите язык:",
                         reply_markup=markup_inline_languages)
        index = value[1]
        checkStatus[call.message.chat.id][index] = call.data
    else:
        markup_inline = types.InlineKeyboardMarkup()
        firstButton, secondButton, txt, index = value
        markup_inline.add(listButtonChat[firstButton], listButtonChat[secondButton])
        bot.send_message(call.message.chat.id, txt, reply_markup=markup_inline)
        checkStatus[call.message.chat.id][index] = call.data


def createButtonChat():
    for k, v in {'finance': '📊 Сфера финансов', 'it': '🖥 Сфера IT',
                 'management': '👱🏻‍♂ Менеджмент',
                 'accounting': '🗃 Бухгалтерия', 'gamedesigners': '🎮 Game Design',
                 'developers': '💻 Developer',
                 'crisisAnalytics': 'Кризисная аналитика', 'registration': 'Бухгалтерский учёт',
                 'state': 'Государственный', 'entrepreneurial': 'Предпринимательский'}.items():
        listButtonChat[k] = types.InlineKeyboardButton(text=v, callback_data=k)


def print_vacancy(chat_id, start_index, end_index):
    for i in range(start_index, end_index):
        vacancy = vacancies[chat_id][0][i]
        salary = vacancy[1].split(' - ')
        place = f'Ближайшая станция метро: {vacancy[0]}'

        message = f'Заработная ставка от {salary[0]} и до {salary[1]} рублей.\n'
        message += f'{place}\n'
        message += f'Ссылка на вакансию: {vacancy[2]}.\n'
        bot.send_message(chat_id, message)


def createButtonKeyboard():
    languages = {'Python': ['G', 'D'], 'C++': ['G', 'D'], 'C#': ['G', 'D'], 'Swift': ['G', 'D'],
                 'Java': ['G', 'D'],
                 'Assembler': ['G'], 'Rust': ['D'], 'JavaScript': ['D'], 'SQL': ['D'],
                 'Kotlin': ['D']}

    for language, fields in languages.items():
        for field in fields:
            listKeyboardLanguages[field].append(
                types.InlineKeyboardButton(text=language, callback_data=language))

    for district in nameDistricts:
        massKeyboardDistrict.append(
            types.InlineKeyboardButton(text=district, callback_data=district))


if __name__ == '__main__':
    createButtonChat()
    createButtonKeyboard()
    bot.polling()
