from PyQt5.QtWidgets import QWidget, QMessageBox
from data.py_files.ui_code import Ui_AllFilms
from windows.admin_windows.create_film import CreateFilm
from windows.admin_windows.create_afisha import CreateAfisha
from windows.base_functions import connection, cursor, create_table


class AllFilms(QWidget, Ui_AllFilms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_film = CreateFilm()
        self.setFixedWidth(710)
        self.create_afisha_form = CreateAfisha()
        self.initUI()

    def initUI(self) -> None:
        self.update_button.clicked.connect(self.load_film_data)
        self.add_film_button.clicked.connect(self.add_film)
        self.delete_film_button.clicked.connect(self.delete_film)
        self.create_afisha_button.clicked.connect(self.create_afisha)
        self.load_film_data()

    def create_afisha(self) -> None:
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        film_name = self.film_table_data.item(row, 1).text()
        genre_id, afisha_id = cursor.execute(f"SELECT genres.id, films.afisha "
                                             f"FROM films "
                                             f"INNER JOIN genres ON genres.id = films.genre "
                                             f"WHERE films.name='{film_name}'").fetchone()
        if afisha_id:
            valid = QMessageBox.question(self, "Афиша",
                                         "У данного сеанса уже есть афиша, удалить и перезаписать?",
                                         QMessageBox.Yes, QMessageBox.No)
            if valid != QMessageBox.Yes:
                return
            cursor.execute(f"UPDATE films SET afisha=NULL WHERE name=? and genre={genre_id}", (film_name, ))
            cursor.execute(f"DELETE FROM descriptions WHERE id={afisha_id}")
            connection.commit()

        self.create_afisha_form.film_name = film_name
        self.create_afisha_form.genre_id = genre_id
        self.create_afisha_form.show()

    def load_film_data(self) -> None:
        query_result = cursor.execute(f"SELECT "
                                      f"films.id, films.name, genres.name, films.duration, "
                                      f"films.datetime, cinemas.name, rooms.id, films.price "
                                      f"FROM films "
                                      f"INNER JOIN genres ON genres.id = films.genre "
                                      f"INNER JOIN cinemas ON cinemas.id = films.cinema "
                                      f"INNER JOIN rooms ON rooms.id = films.room "
                                      f"WHERE films.can_buy = 1 "
                                      f"ORDER BY films.name;").fetchall()

        if query_result:
            titles = ["ИД", "Название фильма", "Жанр", "Время", "Начало", "Кинотеатр", "Зал", "Цена"]
            create_table(titles, query_result, self.film_table_data, equal_cols=False, need_datetime=True, column=4)
            self.film_table_data.setColumnWidth(1, 160)
            self.film_table_data.setColumnWidth(6, 30)
            self.film_table_data.setColumnWidth(7, 30)
            self.film_table_data.setColumnWidth(0, 20)
            self.film_table_data.setColumnWidth(3, 97)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.film_table_data.rowCount() > 0:
            self.film_table_data.removeRow(0)

    def add_film(self) -> None:
        self.create_film.setWindowTitle("Добавление сеанса")
        self.create_film.show()

    def delete_film(self) -> None:
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, 'Удаление сеанса', "Действительно удалить данный сеанс?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            film_id = int(self.film_table_data.item(row, 0).text())
            cursor.executescript(f"UPDATE films SET can_buy = 0 WHERE id={film_id}; "
                                 f"DELETE FROM seats WHERE film={film_id}")
            connection.commit()
            self.load_film_data()
