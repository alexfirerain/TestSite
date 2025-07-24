import os, sqlite3

from flask import Flask, url_for, request, render_template, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_manager, current_user, login_required
from werkzeug.utils import secure_filename

from forms.consider_form import ConsiderForm
from site_repository import *

from data import db_session
from data.consideration_model import Consideration
from data.user_model import User
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, logout_user

app = Flask(__name__)
# repo = SiteRepository('db/site_database.sqlite')

login_manager = LoginManager()
login_manager.init_app(app)

debug = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = ('readthefuckingmanualonlythenfuck')
PIC_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_pic_ext(filename: str) -> bool:
    return ('.' in filename
            and filename.rsplit('.', 1)[1].lower() in PIC_EXTENSIONS)

def actual_appeal():
    return current_user.name if current_user.is_authenticated else 'Гость'


@app.route('/')
@app.route('/index')
def index():
    params = {
        'title': 'Приветствие',
        'user': actual_appeal(),
        'weather': 'погодка ништяк'
    }
    return render_template('index.html', **params)

@login_manager.user_loader
def load_user(user_id):
    # db_sess = db_session.create_session()
    # return db_sess.query(User).get(user_id)
    return get_user_by_id(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = LoginForm()
    if l_form.validate_on_submit():
        user = get_user_by_email(l_form.email.data)
        if user and user.check_password(l_form.password.data):
            # успешный вход
            login_user(user, remember=l_form.remember_me.data)
            return redirect('/')
        elif user:
            l_form.password.errors.append('Неверный пароль')
        else:
            # пользователь не найден
            l_form.email.errors.append('Пользователь с такой почтой не зарегистрирован')

    return render_template('login.html',
                           title='Неуспешный вход',
                           form=l_form,
                           message=request.args.get('message'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    r_form = RegisterForm()
    if r_form.validate_on_submit():
        # если пароли не совпали
        if r_form.password.data != r_form.password_repeat.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   message='Пароли не совпадают',
                                   form=r_form)

        # Если пользователь с таким E-mail в базе уже
        if get_user_by_email(r_form.email.data) is not None:
            return render_template('register.html',
                                   title='Регистрация',
                                   message='Пользователь с такой почтой уже зарегистрирован',
                                   form=r_form)
        user = User(
            name=r_form.name.data,
            email=r_form.email.data,
            about=r_form.self_description.data
        )
        user.set_password(r_form.password.data)
        save_user(user)
        flash('Регистрация кажется успешно завершённой, заходите!')
        return redirect('/login')

    return render_template('register.html',
                           title='Регистрация', form=r_form)




@app.route('/about')
def about():
    return render_template('about.html',
                           title='О нас', user=actual_appeal())


@app.route('/considerations', methods=['GET', 'POST'])
def considerations():
    posts = get_considerations_for_user(current_user.id)\
                if current_user.is_authenticated \
                    else get_all_public_considerations()

    return render_template('considerations.html',
                           title='Разные соображения', user=actual_appeal(), posts=posts)


@app.route('/consider', methods=['GET', 'POST'])
@login_required
def consider():
    # if not current_user.is_authenticated:
    #     return redirect(url_for('login'))

    c_form = ConsiderForm()
    if c_form.validate_on_submit():
        consideration = Consideration(
            title=c_form.title.data,
            content=c_form.content.data,
            is_private=c_form.is_private.data,
            # author=current_user.id
        )
        thinker = get_user_by_id(current_user.id)
        # print(thinker.id)
        thinker.considerations.append(consideration)
        # update_user(thinker)
        if save_consideration(consideration):  # Предполагается, что у вас есть такой метод
            flash('Ваша мысль сохранена!', 'success')
            return redirect(url_for('considerations'))
        else:
            flash('Не удалось сохранить мысль.', 'danger')

    return render_template('consider.html',
                           title='Фиксация мысли',
                           who=actual_appeal(),
                           form=c_form)



# @app.route('/form', methods=['GET', 'POST'])
# def form_test():
#     if request.method == 'GET':
#         with open('templates/form.html', 'r', encoding='utf-8') as h:
#             return h.read()
#     elif request.method == 'POST':
#         result = request.form
#         print(result['gender'])
#         print(result['email'])
#         print(result['accept'])
#         print(result)
#
#         file = request.files['file']
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#
#         return "Форма успешно отправлена!<br>", '200 OK'
#     return 'Такая тема не воспринимается сервером', '405 METHOD NOT ALLOWED'


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
        if file and allowed_pic_ext(filename):
            proper_name = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], proper_name))
            return f'Файл {filename} успешно загружен!<br>'
    return 'Ошибка загрузки', '400 BAD REQUEST'


@app.errorhandler(404)
def not_found(e):
    return render_template('errorpage.html', title='Неизвестная страница', code=404), '404 NOT FOUND'


@app.errorhandler(500)
def server_error(e):
    return (render_template('errorpage.html', title='Ошибка на сайте, к сожалению', code=500),
            '500 INTERNAL SERVER ERROR')


def create_default_admin():
    """Создать админа, если его нет"""
    if is_users_table_empty():
        admin = User(
            name="admin",
            email="s@w.a",
            about="тестовый админ",
            level=1
        )
        admin.set_password("111")  # Можно поменять на любой пароль
        save_user(admin)
        print("Создан администратор по умолчанию")


if __name__ == '__main__':
    db_session.global_init('db/site_database.sqlite')
    create_default_admin()
    app.run(host='localhost', port=5000, debug=debug)
