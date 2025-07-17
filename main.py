import os, sqlite3

from flask import Flask, url_for, request, render_template
from werkzeug.utils import secure_filename

from crud import TripRepository

app = Flask(__name__)
db = TripRepository('db/trippers.sqlite', 'users')

debug = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = ('В пуранической вистoрии пахтанья Молочного океана дэвы и aсуры'
                            'испольzовали Мандару как мутовку, а $ме́я Васуки — как верёвку!')
ALLOWED_EXTENSIONS = {'txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', '7z'}


def allowed_file(filename: str) -> bool:
    return ('.' in filename
            and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


@app.route('/')
@app.route('/index')
def index():
    params = {
        'title': 'Приветствие',
        'user': 'Юзер',
        'weather': 'погодка ништяк'
    }
    return render_template('index.html', **params)


@app.route('/about')
def about():
    return render_template('about.html', title='О нас', user='посетитель')


@app.route('/trip/')
def get_all_trippers():
    all_trippers = db.read_all()
    return render_template('trippers.html', title='<Командировочные', trippers=all_trippers) , '200 OK'


@app.route('/trip/<int:trip_id>')
def get_tripper(trip_id=None):
    if trip_id is None:
        return get_all_trippers()
    else:
        tripper = db.read_by_id(trip_id)
        params = {
            "id": tripper[0],
            "name": tripper[1],
            "destination": tripper[2],
            "costs": tripper[3],
            "since": tripper[4],
            "till": tripper[5]
        }
        return render_template('tripper.html', title='<Командировочные', **params), '200 OK'


@app.route('/form', methods=['GET', 'POST'])
def form_test():
    if request.method == 'GET':
        with open('templates/form.html', 'r', encoding='utf-8') as h:
            return h.read()
    elif request.method == 'POST':
        result = request.form
        print(result['gender'])
        print(result['email'])
        print(result['accept'])
        print(result)

        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return "Форма успешно отправлена!<br>", '200 OK'
    return 'Такая тема не воспринимается сервером', '405 METHOD NOT ALLOWED'


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'GET':
        with open('templates/uploading.html', 'r', encoding='utf-8') as h:
            return h.read()
    elif request.method == 'POST':
        if 'file' not in request.files:
            return 'Файл не выбран', '400 BAD REQUEST'

        filename = request.files['file'].filename
        file = request.files['file']

        if filename == '':
            return 'Файл без имени', '400 BAD REQUEST'
        if file and allowed_file(filename):
            proper_name = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], proper_name))
            return f'Файл {filename} успешно загружен!<br>'
    return 'Ошибка загрузки', '400 BAD REQUEST'




if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=debug)
