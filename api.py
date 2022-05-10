# -*- coding: utf-8 -*-
import requests
import json
import sqlite3


class Database:
    def __init__(self, filename):
        self.filename_database = filename
        self.connect = sqlite3.connect(self.filename_database, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def read(self, tableName):
        try:
            db = sqlite3.connect(self.filename_database)
            cursor = db.cursor()
            query = f"""SELECT place,salary,link FROM {tableName};"""
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
        self.cursor.execute(f"""INSERT INTO {table_name}(specialization, place, salary, link)
                                VALUES ('{params[0]}', '{params[1]}',
                                '{params[2]}', '{params[3]}');""")
        self.connect.commit()

    def clear_database(self, table_name):
        self.cursor.execute(f'DELETE FROM {table_name};')
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


def search_profession(database, table_name, profession, specialization, remote_work=False):
    max_pages = 1000
    database.clear_database(table_name)
    try:
        for index_page in range(max_pages):
            page = get_page(profession, index_page)
            json_object = json.loads(page)
            for vacancy in json_object['items']:
                salary = vacancy['salary']
                if salary is None:
                    continue
                if salary['currency'] != 'RUR':
                    continue
                if salary['from'] is None or salary['to'] is None:
                    continue
                if remote_work:
                    if vacancy['address'] is not None:
                        continue
                    params = [specialization, 'Удалённая работа',
                              str(vacancy['salary']['from']) + ' - ' + str(vacancy['salary']['to']),
                              vacancy['alternate_url']]
                else:
                    if vacancy['address'] is None:
                        continue
                    if vacancy['address']['metro'] is None:
                        continue
                    params = [specialization, vacancy['address']['metro']['station_name'],
                              str(vacancy['salary']['from']) + ' - ' + str(vacancy['salary']['to']),
                              vacancy['alternate_url']]
                database.rewrite_database(params, table_name)
    except:
        pass


database_filename = 'vacancies.db'
db = Database(database_filename)
