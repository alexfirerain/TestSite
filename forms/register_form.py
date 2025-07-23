from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import SubmitField
from wtforms.fields.simple import EmailField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired('Введите Ваше имя')])
    email = EmailField('Почта', validators=[DataRequired('Введите корректный Email')])
    password = PasswordField('Пароль', validators=[DataRequired('Пароль обязателен')])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired('Нужно подтвердить пароль')])
    self_description = TextAreaField('Немного о себе')
    submit = SubmitField('Регистрация')
