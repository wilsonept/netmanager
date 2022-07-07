from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

"""Файл с формами приложения."""


# ------ Формы ---------------------------------------------------------

class LoginForm(FlaskForm):
    """Форма авторизации."""
    name = StringField(label="Логин", validators=[DataRequired()])
    passwd = PasswordField(label="Пароль", validators=[DataRequired()])
    submit = SubmitField(label="Submit")