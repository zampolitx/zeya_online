from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
menu = [{"name":'Сегодня', "url": "today"},
        {"name":'Блог', "url": "blog"},
        {"name":'Про нас', "url": "about"}]

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdlkjOJSDFlksdlkfDSFOol.ksdjf'

@app.route('/')
def index():
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

if __name__=="__main__":
    app.run(debug=True)