# -*- coding: utf-8 -*-
import requests
import json
import sqlite3


def open_json(filename):
    with open(filename, 'r', encoding='UTF-8') as file:
        f = file.read()
        data = json.loads(f)
    return data


TRANSLATE = {'crisisAnalytics': 'Кризисная аналитика', 'registration': 'Бухгалтерский учёт',
             'state': 'Государственный менеджмент', 'entrepreneurial': 'Государственный менеджмент'}
DISTRICTS = open_json('districts.json')


class Database:
    def __init__(self, filename):
        self.filename_database = filename
        self.connect = sqlite3.connect(self.filename_database, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def read(self, chat_id, tableName):
        try:
            db = sqlite3.connect(self.filename_database)
            cursor = db.cursor()
            query = f"""SELECT place,salary,link FROM {tableName} WHERE chat_id={chat_id};"""
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
        except sqlite3.Error as err:
            print("DB error:", err)
            data = []
        finally:
            if db:
                db.close()
            return data

    def rewrite_database(self, params, table_name):
        self.cursor.execute(f"""INSERT INTO {table_name}(chat_id, specialization, place, salary, link)
                                VALUES ('{params[0]}', '{params[1]}',
                                '{params[2]}', '{params[3]}', '{params[4]}');""")
        self.connect.commit()

    def clear_database(self, chat_id, table_name):
        self.cursor.execute(f'DELETE FROM {table_name} WHERE chat_id={chat_id};')
        self.connect.commit()


def get_page(text, page=0):
    params = {
        'text': text,
        'area': 1,
        'page': page,
        'per_page': 100
    }
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data


def search_profession(chat_id, database, table_name, profession, specialization, district):
    max_pages = 1000
    database.clear_database(chat_id, table_name)
    if profession == 'it':
        specialization = f'Разработчик {specialization}'
    else:
        specialization = TRANSLATE[specialization]
    try:
        for index_page in range(max_pages):
            page = get_page(specialization, index_page)
            json_object = json.loads(page)
            for vacancy in json_object['items']:
                salary = vacancy['salary']
                if salary is None:
                    continue
                if salary['currency'] != 'RUR':
                    continue
                if salary['from'] is None or salary['to'] is None:
                    continue
                if vacancy['address'] is None:
                    continue
                if vacancy['address']['metro'] is None:
                    continue
                place = vacancy['address']['metro']['station_name']
                if place not in DISTRICTS[district]:
                    continue
                params = [chat_id, specialization, place,
                          str(vacancy['salary']['from']) + ' - ' + str(vacancy['salary']['to']),
                          vacancy['alternate_url']]
                database.rewrite_database(params, table_name)
    except:
        pass
