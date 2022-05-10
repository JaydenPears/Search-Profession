# -*- coding: utf-8 -*-
# import modules:
from api import search_profession, db

# import libraries:
import telebot
from telebot import types
# ВОВА, ВЕРНИ СНИКЕРС!!!! ОН ХОЧЕТ ОСТАТЬСЯ ДЕВСТВЕННИКОМ!!!!
#
#
# P.S. ШУЧУ) 
#P.S.S ИЛИ НЕТ >:(

LANGUAGES = ['Python', 'Rust', 'C++', 'C#', 'JS', 'SQL', 'Swift', 'Kotlin', 'Java', 'Assembler']
TRANSLATE = {'developer': 'разработчик', 'gamedesigner': 'геймдзиайнер'}
bot = telebot.TeleBot("5367028014:AAEKarGWXV5Zu0ybZsRkxGui00ILp6S388Y")
massButtonChat = {}
massButtonKeyboardG = []
massButtonKeyboardD = []
save = 0
path = []


@bot.message_handler(commands=["start"])
def start(message):
    text_hello = 'Доброго времени суток! Я бот для поиска работы, созданный специально для помощи в этом молодым ' \
                 'специалистам в городе Москва.'
    bot.send_message(message.chat.id, text_hello)

    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(massButtonChat['work'], massButtonChat['sideJob'])
    bot.send_message(message.chat.id, "Напиши команду /help для того, чтобы получить " \
                                      "инструкцию по использованию моих функций. ", reply_markup=markup_inline)


@bot.message_handler(commands=["help"])
def help(message):
    text_hello = 'Ваши вопросы и пожелания просьба направлять на нашу почту: tgbotsearchforjob@gmail.com.'
    bot.send_message(message.chat.id, text_hello)


@bot.message_handler(content_types=["text"])
def text_handler(message):
    global path
    search_profession(db, path[2] + 's', f'{message.text} {TRANSLATE[path[2]]}', message.text, path[3])
    vacancies = db.read(path[2] + 's')  # Список, как список data в примере красивой печати
    for vacancy in vacancies:
        salary = vacancy[1].split()
        if vacancy[0] == 'Удалённая работа':
            place = 'Работа в удалённой форме.'
        else:
            place = f'Ближайшая станция метро: {vacancy[0]}'
        message = f'Заработная ставка от {salary[0]} и до {salary[1]} рублей.\n'
        message += f'{place}\n'
        message += f'Ссылка на вакансию: {vacancy[2]}.\n'
        message += f'-------------'
    path = []
		bot.send_message(call.message.chat.id,text=message)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global save, path

    if call.data == "work":
        markup_inline_work = types.InlineKeyboardMarkup()
        markup_inline_work.add(massButtonChat['finance'], massButtonChat['it'])
        bot.send_message(call.message.chat.id, "Выберите сферу работы:", reply_markup=markup_inline_work)
        path.append(call.data)
    elif call.data == "sideJob":
        pass
    elif call.data == "finance":
        markup_inline_finance = types.InlineKeyboardMarkup()
        markup_inline_finance.add(massButtonChat['accounting'], massButtonChat['management'])
        bot.send_message(call.message.chat.id, "Выберите сферу финансов:", reply_markup=markup_inline_finance)
        path.append(call.data)
    elif call.data == "it":
        markup_inline_it = types.InlineKeyboardMarkup()
        markup_inline_it.add(massButtonChat['gameDesign'], massButtonChat['developer'])
        bot.send_message(call.message.chat.id, "Выбери профессию:", reply_markup=markup_inline_it)
        path.append(call.data)
    elif call.data == "gameDesign":
        save = 'G'
        markup_inline_it_next = types.InlineKeyboardMarkup()
        markup_inline_it_next.add(massButtonChat['distantWork'], massButtonChat['spaceWork'])
        bot.send_message(call.message.chat.id, "Режим работы:", reply_markup=markup_inline_it_next)
        path.append(call.data)
    elif call.data == "developer":
        save = 'D'
        markup_inline_it_next = types.InlineKeyboardMarkup()
        markup_inline_it_next.add(massButtonChat['distantWork'], massButtonChat['spaceWork'])
        bot.send_message(call.message.chat.id, "Режим работы:", reply_markup=markup_inline_it_next)
        path.append(call.data)
    elif call.data == "distantWork":
        markup_inline_it_next_workD = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if save == 'D':
            main_mass = massButtonKeyboardD
        else:
            main_mass = massButtonKeyboardG

        for i in range(0, len(main_mass), 3):
            markup_inline_it_next_workD.add(main_mass[i], main_mass[i + 1], main_mass[i + 2])

        bot.send_message(call.message.chat.id, 'Выбери язык:', reply_markup=markup_inline_it_next_workD)
        path.append(call.data)
    elif call.data == "spaceWork":
        markup_inline_it_next_workS = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if save == 'D':
            main_mass = massButtonKeyboardD
        else:
            main_mass = massButtonKeyboardG

        for i in range(0, len(main_mass), 3):
            markup_inline_it_next_workS.add(main_mass[i], main_mass[i + 1], main_mass[i + 2])

        bot.send_message(call.message.chat.id, "Выбери язык:", reply_markup=markup_inline_it_next_workS)
        path.append(call.data)
    elif call.data == "accounting":
        path.append(call.data)
        path.append(False)
        search_profession(db, path[2], f'Бухгалтерский учёт', 'Accounting')
        vacancies = db.read(path[2])  # Список, как список data в примере красивой печати
        path = []
			for vacancy in vacancies:
        salary = vacancy[1].split()
        if vacancy[0] == 'Удалённая работа':
            place = 'Работа в удалённой форме.'
        else:
            place = f'Ближайшая станция метро: {vacancy[0]}'
        message = f'Заработная ставка от {salary[0]} и до {salary[1]} рублей.\n'
        message += f'{place}\n'
        message += f'Ссылка на вакансию: {vacancy[2]}.\n'
        message += f'-------------'
    
			bot.send_message(call.message.chat.id,text=message)
    elif call.data == "management":
        path.append(call.data)
        path.append(False)
        search_profession(db, path[2], f'Менеджмент', 'Management')
        vacancies = db.read(path[2])  # Список, как список data в примере красивой печати
        path = []
				for vacancy in vacancies:
        	salary = vacancy[1].split()
        	if vacancy[0] == 'Удалённая работа':
            place = 'Работа в удалённой форме.'
        	else:
            place = f'Ближайшая станция метро: {vacancy[0]}'
        	message = f'Заработная ставка от {salary[0]} и до {salary[1]} рублей.\n'
        	message += f'{place}\n'
        	message += f'Ссылка на вакансию: {vacancy[2]}.\n'
        	message += f'-------------'
    
				bot.send_message(call.message.chat.id,text=message)
			
			

def createButtonChat():
    massButtonChat['work'] = types.InlineKeyboardButton(text="💰 Работа", callback_data="work")
    massButtonChat['sideJob'] = types.InlineKeyboardButton(text="🪙 Подработка", callback_data="sideJob")

    massButtonChat['finance'] = types.InlineKeyboardButton(text="📊 Сфера финансов", callback_data="finance")
    massButtonChat['it'] = types.InlineKeyboardButton(text="🖥 Сфера IT", callback_data="it")

    massButtonChat['management'] = types.InlineKeyboardButton(text="👱🏻‍♂ Менеджмент", callback_data="management")
    massButtonChat['accounting'] = types.InlineKeyboardButton(text="🗃 Бухгалтерия", callback_data="accounting")

    massButtonChat['gameDesign'] = types.InlineKeyboardButton(text="🎮 Game Design", callback_data="gameDesign")
    massButtonChat['developer'] = types.InlineKeyboardButton(text="💻 Developer", callback_data="developer")

    massButtonChat['distantWork'] = types.InlineKeyboardButton(text="🏠 Удалённая работа", callback_data='distantWork')
    massButtonChat['spaceWork'] = types.InlineKeyboardButton(text="🏢 Space work", callback_data='spaceWork')


def createButtonKeyboard():
    g = ['Python', 'C++', 'C#', 'Swift', 'Java', 'Assembler']
    d = ['Python', 'Rust', 'C++', 'C#', 'VS', 'SQL', 'Swift', 'Kotlin', 'Java']

    for i in range(len(g)):
        massButtonKeyboardG.append(types.KeyboardButton(g[i]))

    for i in range(len(d)):
        massButtonKeyboardD.append(types.KeyboardButton(d[i]))


if __name__ == '__main__':
    createButtonChat()
    createButtonKeyboard()
    bot.polling()