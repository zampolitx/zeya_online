from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import os
import sqlite3

# Конфигурация
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'sdlkjOJSDFlksdlkfDSFOol.ksdjf'

menu = [{"name":'Сегодня', "url": "today"},
        {"name":'Блог', "url": "blog"},
        {"name":'Про нас', "url": "about"}]

app = Flask(__name__)
app.config.from_object(__name__)                # Загружаем конфигурацию
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))          # переопределяем путь к базе данных, app.root_path - текущий каталог приложения

# Функция установления соединения с базой данных
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])              # app.config['DATABASE'] - путь, где расположена база данных
    conn.row_factory = sqlite3.Row                              # Записи из БД будут представлены не в виде кортэжей, а в виде словаря
    return conn

# Функция для создания таблиц БД, без запуска вэб сервера. Нужно вызывать через консоль
def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

# Функция соединения с БД, если еще соединения нет, g - переменная контекста приложения
def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route('/')
def index():
    db = get_db()       # Устанавливаем соединение с БД
    return render_template("index.html", title='Главная страница', menu=menu)

@app.route('/today')
def today():
    return render_template("today.html", title='Сегодня', menu=menu)

@app.route('/about', methods=["POST", "GET"])
def about():
    if request.method == "POST":
        if len(request.form['username']) > 2:                               # Начало блока мгновенных сообщений
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправления', category='error')
    return render_template("about.html", title='О сайте', menu=menu)

@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] !=username:     # Если пользователь не залогинился или пытается войти под чужой учеткой
        abort(401)
    return f'Профиль пользователя: {username}'

@app.route('/login', methods=['POST', 'GET'])                               # Обработчик входа в учетку
def login():
    if 'userLogged' in session:                                             # Если пользователь уже есть в сессии
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'zampolit' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=menu)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu), 404         # Если не поставить 404 то код будет 200, а не 404

@app.teardown_appcontext            # Декоратор срабатывает тогда, когда происходит уничтожение контекста приложения
def close_db(error):
    if hasattr(g, 'link_db'):       # Закрываем соединение с БД, если оно было установлено ранее
        g.link_db.close()           # Обращаемся к соединению и вызываем метод close()

if __name__=="__main__":
    app.run(debug=True)