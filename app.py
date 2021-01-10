from flask import Flask, render_template, url_for, request
menu = [{"name":'Сегодня', "url": "today"},
        {"name":'Блог', "url": "blog"},
        {"name":'Про нас', "url": "about"}]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", title='Главная страница', menu=menu)

@app.route('/today')
def today():
    return render_template("today.html", title='Сегодня', menu=menu)

@app.route('/about', methods=["POST", "GET"])
def about():
    if request.method == "POST":
        print(request.form)
    return render_template("about.html", title='О сайте', menu=menu)


if __name__=="__main__":
    app.run(debug=True)