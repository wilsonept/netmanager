from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user

from application import app, LOGIN_MANAGER as log_man
from models import User
from forms import LoginForm

"""Файл запуска приложения/файл маршрутов."""


@log_man.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# ------- Маршруты приложения ------------------------------------------

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if not current_user.is_anonymous and current_user.id == 1: 
        return render_template("admin.html")
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Аутентификация пользователя.
            user = User.query.filter_by(name=form.name.data).first()

            if user:
                # Авторизация пользователя.
                if user.passwd == form.passwd.data:
                    login_user(user)

                    return redirect(url_for("home"))

            flash("Не верный логин или пароль, повторите попытку.")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    # TODO Выход из пользователя.
    pass


# ------- Маршруты API -------------------------------------------------

# TODO Получение информации о состоянии интерфейса.
# TODO Включение/выключение интерфейса.
# TODO Добавление/удаление адреса.
# TODO Изменение адреса.
# TODO Изменение маски.

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)