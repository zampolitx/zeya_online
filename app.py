from flask import Flask, render_template, url_for, request, flash
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


if __name__=="__main__":
    app.run(debug=True)