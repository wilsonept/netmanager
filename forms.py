from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms import BooleanField, FieldList, FormField
from wtforms.validators import DataRequired, StopValidation

"""Файл с формами приложения."""


# ------ Формы ---------------------------------------------------------

class MyDataRequired(DataRequired):
    """Полный аналог суперкласса, но на русском."""
    def __call__(self, form, field):
        if field.data and (not isinstance(field.data, str) or field.data.strip()):
            return

        if self.message is None:
            message = field.gettext("Это поле необходимо.")
        else:
            message = self.message

        field.errors[:] = []
        raise StopValidation(message)


class LoginForm(FlaskForm):
    """Форма авторизации."""
    login = StringField(label="Логин", validators=[MyDataRequired()])
    passwd = PasswordField(label="Пароль", validators=[MyDataRequired()])
    submit = SubmitField(label="Войти")


class IPAddressEntryForm(FlaskForm):
    """Форма одной записи IP адреса.  """
    cidr = StringField(validators=[MyDataRequired()])
    delete = BooleanField()

class AdminForm(FlaskForm):
    """Форма администратора."""
    addresses = FieldList(FormField(IPAddressEntryForm), min_entries=0)
    submit = SubmitField(label="Применить")