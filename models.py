import sys

from application import DB as db

"""Файл моделей и логики работы с БД."""


class User(db.Model):
    """Таблица пользователей."""
    __tablename__ = "users"

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(40), nullable=False)
    passwd = db.Column(db.String(40), nullable=False)


def self_db_rebuild(force=False):
    """Пересоздает таблицы в БД."""
    if not force:
        answer = input(
            (
                "Это действие приведет к полной потере данных."
                "Вы действительно хотите перестроить таблицы? [N]/Y "
            ) or "N"
        )
        if answer.capitalize() != "Y":
            print("Прервано пользователем.")
            exit()

    print("[ DROP ] Удаляю все таблицы.")
    db.drop_all()
    print("[ CREATE ] Создаю таблицы.")
    db.create_all()

    # Создаем пользователя.
    db.session.add(User(name="netmanager", passwd="1"))
    db.session.commit()

if __name__ == "__main__":
    if "rebuild" in sys.argv:
        if "force" in sys.argv:
            self_db_rebuild(force=True)
        else:
            self_db_rebuild()