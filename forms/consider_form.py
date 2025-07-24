from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class ConsiderForm(FlaskForm):
    title = StringField('Тема мысли', validators=[DataRequired('Введите заголовок')])
    content = TextAreaField('Содержание мысли')
    is_private = BooleanField('Скрытая')
    submit = SubmitField('Записать')
