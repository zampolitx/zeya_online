import sqlite3
import time
import math
from flask import url_for
import re

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []                           # Если исключение, то возвращаем пустой список

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")      # сравниваем введенный url с дубликатами из БД
            res = self.__cur.fetchone()
            if res['count'] > 0:                                                                    # Если статья с таким url уже существует, то
                print("Статья уже существует")
                return False
            tm = math.floor(time.time())    # Округляем текущее время до секунд и записываем в tm
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)', (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД'+str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:                                     # Если статья нашлась в БД
                base = url_for('static', filename='img')
                text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                              "\\g<tag>" + base + "/\\g<url>>",
                              res['text'])
                return res                              # Возвращаем статью в виде кортэжа
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))

        return []