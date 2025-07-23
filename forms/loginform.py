from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('Логин', validators=[DataRequired('укажите почту регистрации')])
    password = PasswordField('Пароль', validators=[DataRequired('укажите пароль')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
