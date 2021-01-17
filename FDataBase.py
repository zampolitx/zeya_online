import sqlite3
import time
import math

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

    def addPost(self, title, text):
        try:
            tm = math.floor(time.time())    # Округляем текущее время до секунд и записываем в tm
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?)', (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД'+str(e))
            return False
        return True

    def getPost(self, postID):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {postID} LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if res:                                     # Если статья нашлась в БД
                return res                              # Возвращаем статью в виде кортэжа
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))
        return (False, False)

    def getPostsAnonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД" + str(e))

        return []