from PyQt5.QtWidgets import QWidget, QMessageBox
from data.py_files.ui_code import Ui_UserFilms
from windows.user_windows.afisha_view import AfishaView
from windows.user_windows.room_view import RoomView
from windows.base_functions import cursor, create_table


class UserFilms(QWidget, Ui_UserFilms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.user_id = None
        self.room = RoomView()
        self.search_button.clicked.connect(self.search)
        self.afisha_button.clicked.connect(self.watch_afisha)
        self.buy_ticket_button.clicked.connect(self.watch_room)
        self.search_by_box.addItem("Нет")
        self.search_by_box.addItem("Кинотеатр")
        self.search_by_box.addItem("Название")
        self.search_by_box.addItem("Жанр")
        self.search_by_box.addItem("Максимальная цена")
        self.base_query = f"SELECT films.id, films.name, genres.name, films.duration, " \
                          f"films.datetime, cinemas.name, rooms.id, films.price FROM " \
                          f"films INNER JOIN genres ON genres.id = films.genre INNER " \
                          f"JOIN cinemas ON cinemas.id = films.cinema INNER JOIN rooms " \
                          f"ON rooms.id = films.room WHERE films.can_buy = 1 "
        self.query = self.base_query[:]
        self.order = " ORDER BY films.datetime"
        self.load_films_data()
        self.afisha_view = AfishaView()

    def search(self) -> None:
        search_by = self.search_by_box.currentText()
        search_text = self.search_edit.text()

        if search_by == 'Нет':
            self.query = self.base_query[:]

        if search_text:
            if search_by == "Кинотеатр":
                self.query = self.base_query + f" and cinemas.name LIKE '%{search_text}%'"
            elif search_by == "Название":
                self.query = self.base_query + f" and films.name LIKE '%{search_text}%'"
            elif search_by == "Жанр":
                self.query = self.base_query + f" and genres.name LIKE '%{search_text}%'"
            elif search_by == "Максимальная цена" and search_text.isdigit():
                self.query = self.base_query + f" and films.price <= {int(search_text)}"
        self.load_films_data()

    def load_films_data(self) -> None:
        query_result = cursor.execute(self.query + self.order).fetchall()

        if query_result:
            titles = ["ИД", "Название фильма", "Жанр", "Время", "Начало", "Кинотеатр", "Зал", "Цена"]
            create_table(titles, query_result, self.films_table_data, equal_cols=False, need_datetime=True, column=4)
            self.films_table_data.setColumnWidth(1, 160)
            self.films_table_data.setColumnWidth(6, 48)
            self.films_table_data.setColumnWidth(7, 60)
            self.films_table_data.setColumnWidth(0, 20)
            self.films_table_data.setColumnWidth(3, 97)
        else:
            self.clear_table()

    def watch_afisha(self) -> None:
        row = self.films_table_data.currentRow()
        if row == -1:
            return

        film_id = int(self.films_table_data.item(row, 0).text())
        afisha = cursor.execute("SELECT films.name, genres.name, descriptions.description, "
                                "descriptions.image "
                                "FROM descriptions "
                                f"INNER JOIN films ON films.afisha = descriptions.id and films.id = {film_id} "
                                f"INNER JOIN genres ON genres.id = films.genre").fetchone()
        if afisha:
            self.afisha_view.fill(*afisha)
            self.afisha_view.show()
        else:
            QMessageBox.warning(
                self, 'Афиша', "На этот фильм еще нет афиши",
                QMessageBox.Ok)

    def watch_room(self):
        row = self.films_table_data.currentRow()
        if row == -1:
            return
        film_id = int(self.films_table_data.item(row, 0).text())
        price = int(self.films_table_data.item(row, 7).text())

        self.room.fill(film_id, price, self.user_id)
        self.room.show()

    def clear_table(self) -> None:
        while self.films_table_data.rowCount():
            self.films_table_data.removeRow(0)
