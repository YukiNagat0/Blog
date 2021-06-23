from flask_wtf import FlaskForm

from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class EditPostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(message='Поле должно быть заполнено!')])
    image = FileField('Фотография')
    text = TextAreaField('Текст', validators=[DataRequired(message='Поле должно быть заполнено!')])
    author = StringField('Автор', validators=[DataRequired(message='Поле должно быть заполнено!')])

    submit = SubmitField('Добавить')
