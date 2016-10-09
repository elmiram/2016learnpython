from flask import Flask
from flask import url_for, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return '<html><body><p>Привет, мир!</p></body></html>'


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

if __name__ == '__main__':
    app.run(debug=True)