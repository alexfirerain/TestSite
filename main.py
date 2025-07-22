import os, sqlite3

from flask import Flask, url_for, request, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_manager, current_user
from werkzeug.utils import secure_filename

from crud import TripRepository

from data import db_session
from data.news import News
from data.users import User
from forms.loginform import LoginForm
from forms.user import Register
from flask_login import LoginManager, login_user, logout_user

app = Flask(__name__)
# db = TripRepository('db/trippers.sqlite', 'users')

login_manager = LoginManager()
login_manager.init_app(app)

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
    visitor = current_user.name if current_user.is_authenticated else 'Юзер'
    params = {
        'title': 'Приветствие',
        'user': visitor,
        'weather': 'погодка ништяк'
    }
    return render_template('index.html', **params)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = LoginForm()
    if l_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == l_form.email.data).first()
        if user and user.check_password(l_form.password.data):
            login_user(user, remember=l_form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               message='Неверный логин или пароль',
                               title='Ошибка авторизации',
                               form=l_form)
    return render_template('login.html', title='Авторизация', form=l_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Register()
    if form.validate_on_submit():  # тоже самое, что и request.method == 'POST'
        # если пароли не совпали
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   message='Пароли не совпадают',
                                   form=form)

        db_sess = db_session.create_session()

        # Если пользователь с таким E-mail в базе уже есть
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   message='Такой пользователь уже есть',
                                   form=form)
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация', form=form)




@app.route('/about')
def about():
    return render_template('about.html', title='О нас', user='посетитель')


# @app.route('/trip/')
# def get_all_trippers():
#     all_trippers = db.read_all()
#     return render_template('trippers.html', title='<Командировочные', trippers=all_trippers), '200 OK'
#
#
# @app.route('/trip/<int:trip_id>')
# def get_tripper(trip_id=None):
#     if trip_id is None:
#         return get_all_trippers()
#     else:
#         tripper = db.read_by_id(trip_id)
#         params = {
#             "id": tripper[0],
#             "name": tripper[1],
#             "destination": tripper[2],
#             "costs": tripper[3],
#             "since": tripper[4],
#             "till": tripper[5]
#         }
#         return render_template('tripper.html', title='<Командировочные', **params), '200 OK'


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


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', title='Неизвестная страница'), '404 NOT FOUND'


if __name__ == '__main__':
    db_session.global_init('db/test_site_db.sqlite')
    app.run(host='localhost', port=5000, debug=debug)
