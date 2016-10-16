import datetime

from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():
    urls = {'главная (эта страница)': url_for('index'),
            'привет (переменные в url)': url_for('hi'),
            'форма (форма и ответ на одном url)': url_for('form'),
            'форма про книги (просто форма)': url_for('books'),
            'спасибо (попадаем сюда только после формы про книги)': url_for('thanks'),
            'время (используем redirect)': url_for('time_redirect'),}
    return render_template('index.html', urls=urls)


@app.route('/hi')
@app.route('/hi/<user>')
def hi(user=None):
    if user is None:
        user = 'friend'
    return '<html><body><p>Привет, ' + user + '!</p></body></html>'


@app.route('/form')
def form():
    if request.args:
        name = request.args['name']
        age = request.args['age']
        st = True if 'student' in request.args else False
        return render_template('answer.html', name=name, age=age, student=st)
    return render_template('question.html')


@app.route('/books')
def books():
    return render_template('books.html')


@app.route('/thanks')
def thanks():
    if request.args:
        name = request.args['name']
        book = request.args['book']
        return render_template('thanks.html', name=name, book=book)
    return redirect(url_for('books'))


@app.route('/time')
def time_redirect():
    h = datetime.datetime.today().hour
    if 10 < h < 18:
        return redirect(url_for('index'))
    return redirect(url_for('hi'))


if __name__ == '__main__':
    app.run(debug=True)