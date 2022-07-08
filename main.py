import re

from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user, login_user, login_required, logout_user

from application import app, conf, LOGIN_MANAGER as log_man
from models import User
from forms import LoginForm, AdminForm
from utils import get_iface_cidrs, set_iface_ip_mask
from utils import set_iface_link, set_iface_ip

"""Файл запуска приложения/файл маршрутов."""


@log_man.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# ------- Маршруты приложения ------------------------------------------

@app.route("/") 
@app.route("/home")
def home():
    if not current_user.is_anonymous and current_user.id == 1: 
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))


@app.route("/admin", methods=["GET"])
@login_required
def admin():
    cidrs = get_iface_cidrs(conf["iface"])
    
    addresses = {cidr:cidr for cidr in cidrs}
    addresses["new"] = ""
    form = AdminForm(addresses=addresses)
    if current_user.is_authenticated:

        return render_template("admin.html", form=form)
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Аутентификация пользователя.
            user = User.query.filter_by(name=form.login.data).first()

            if user:
                # Авторизация пользователя.
                if user.passwd == form.passwd.data:
                    login_user(user)

                    return redirect(url_for("home"))

            flash("Не верный логин или пароль, повторите попытку.")
    return render_template("login.html", form=form, errors=form.errors)


@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("login"))


# ------- Маршруты API -------------------------------------------------

# TODO Основной маршрут для формы администратора.
@app.route("/update_iface", methods=["POST"])
def update_iface():
    cidrs = get_iface_cidrs(conf["iface"])
    new_cidrs = []
    to_delete = []

    # Получаем заполненые поля из формы.
    for key, value in request.form.items():
        if key.endswith("cidr") and value != "":
            new_cidrs.append(value)

        # Получаем cidr'ы помеченные на удаление.
        if key.endswith("delete"):
            r = re.search("(addresses-\d+)", key)
            to_delete.append(request.form[f"{r.group(0)}-cidr"])

    # Добавляем адрес.
    if len(new_cidrs) > len(cidrs):
        try:
            set_iface_ip(conf, "add", new_cidrs[-1])
        except Exception:
            # TODO Хорошо бы разобраться почему ошибка.
            print('Что то не понятное :(')
    
    # Удаляем помеченные на удаление.
    for cidr in to_delete:
        try:
            set_iface_ip(conf, "del", cidr)
        except Exception:
            # TODO Хорошо бы разобраться почему ошибка.
            print('Что то не понятное :(')

    # Изменяем адреса/маски
    cidrs = get_iface_cidrs(conf["iface"])
    new_cidrs = [cidr for cidr in new_cidrs if not cidr in to_delete]
    for i in range(len(new_cidrs)):
        if new_cidrs[i] != cidrs[i]:
            kwargs = {
                "iface": conf,
                "old_cidr": cidrs[i],
                "cidr": new_cidrs[i]
            }
            try:
                set_iface_ip_mask(**kwargs)
            except Exception:
                # TODO Хорошо бы разобраться почему ошибка.
                print('Что то не понятное :(')
        
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host="localhost", port=5000)