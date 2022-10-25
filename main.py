import csv
import os
import shutil
import sys
from collections import defaultdict
from random import choice
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QMessageBox,
                             QTableWidgetItem, QHeaderView, QFileDialog,
                             QMenu, QMenuBar, QAction, QTableWidget, QPushButton)


connection = sqlite3.connect("CinemaSystemDatabase.db")
cursor = connection.cursor()


def create_admin_windows() -> None:
    """
    creates nessesary windows for admin
    """
    global all_films, all_cinemas, all_genres, \
        all_rooms, main_admin_window, create_film
    all_cinemas = AllCinemas()
    all_films = AllFilms()
    all_genres = AllGenres()
    all_rooms = AllRooms()
    create_film = CreateFilm()
    main_admin_window = AdminMainWindow()


def create_user_window() -> None:
    """
    creates nessesary windows for user
    """
    global user_main_window, afisha_view, user_films, user_profile
    afisha_view = AfishaView()
    user_profile = UserProfile()
    user_films = UserFilms()
    user_main_window = UserMainWindow()


def create_table(titles: list, query_result: list, table: QTableWidget, enable: bool = False) -> None:
    """
    fills table with taken column titles,
    using data from query_result
    :param titles: list
    :param query_result: list
    :param table: QTableWidget
    :param enable: bool
    """
    table.setRowCount(len(query_result))
    table.setColumnCount(len(query_result[0]))

    table.setHorizontalHeaderLabels(titles)

    for i, elem in enumerate(query_result):
        for j, val in enumerate(elem):
            table.setItem(i, j, QTableWidgetItem(str(val)))
            if enable:
                table.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def create_menubar(self) -> None:
        self.menuBar = QMenuBar(self)
        self.menu = QMenu("Меню", self)
        self.login_action = QAction("Смена пользователя", self)
        self.menuBar.addMenu(self.menu)
        self.menu.addAction(self.login_action)
        self.login_action.triggered.connect(self.change_user)
        self.setMenuBar(self.menuBar)

    def change_user(self) -> None:
        login_window.show()
        self.close()


class AdminMainWindow(MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/admin_main_window.ui", self)
        self.setFixedWidth(710)
        self.setWindowTitle("Администрирование")
        self.create_tab_widget()
        self.create_menubar()

    def create_tab_widget(self) -> None:
        self.tabWidget.addTab(all_cinemas, "Кинотеатры")
        self.tabWidget.addTab(all_rooms, "Залы")
        self.tabWidget.addTab(all_films, "Фильмы")
        self.tabWidget.addTab(all_genres, "Жанры")
        self.tabWidget.addTab(AllUsers(), "Пользователи")


class UserMainWindow(MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/user_main_window.ui", self)
        self.setWindowTitle("Пользователь")
        self.create_tab_widget()
        self.create_menubar()

    def create_tab_widget(self) -> None:
        self.tabWidget.addTab(user_films, "Фильмы")
        self.tabWidget.addTab(user_profile, "Мой профиль")


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/login.ui", self)
        self.setWindowTitle("Вход")
        self.initUI()

    def initUI(self) -> None:
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self) -> None:
        login_text = self.login_edit.text()
        password_text = self.password_edit.text()

        if not login_text:
            QMessageBox.critical(
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин",
                QMessageBox.Ok)
            return
        if not password_text:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль",
                QMessageBox.Ok)
            return

        user_obj = cursor.execute(f"SELECT id, admin FROM users WHERE username = ?"
                                  f" and password=?", (login_text, password_text)).fetchone()
        if user_obj:
            user_id, is_admin = user_obj
            self.clear()
            if is_admin:
                create_admin_windows()
                main_admin_window.show()
            else:
                create_user_window()
                user_profile.fill(user_id)
                user_main_window.show()
        else:
            QMessageBox.critical(
                self, 'Ошибка входа', "Неравильный логин или пароль",
                QMessageBox.Ok)
            return

    def register(self) -> None:
        register_window.show()
        self.clear()
        self.close()

    def clear(self) -> None:
        self.close()
        self.login_edit.clear()
        self.password_edit.clear()


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/register.ui", self)
        self.setWindowTitle("Регистрация")
        self.initUI()

    def initUI(self) -> None:
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self) -> None:
        login_window.show()
        self.close()
        self.clear()

    def register(self) -> None:
        login_text = self.login_edit.text()
        password_text = self.password_edit.text()
        password_text_again = self.password_again.text()

        if not login_text:
            QMessageBox.critical(
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин",
                QMessageBox.Ok)
            return
        if not password_text or not password_text_again:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль и подтвердите его",
                QMessageBox.Ok)
            return
        if password_text != password_text_again:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Пароли не совпадают",
                QMessageBox.Ok)
            return

        user_obj = cursor.execute(f"SELECT username FROM users WHERE username = ?",
                                  (login_text, )).fetchall()
        if user_obj:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Такой пользователь уже существует",
                QMessageBox.Ok)
            return

        cursor.execute(f"INSERT INTO USERS(username, password, admin) "
                       f"VALUES(?, ?, 0)",
                       (login_text, password_text))
        QMessageBox.information(
            self, 'Успех', "Успешно создание пользователя!",
            QMessageBox.Ok)
        connection.commit()
        self.clear()

    def clear(self) -> None:
        self.login_edit.clear()
        self.password_edit.clear()
        self.password_again.clear()


class CreateFilm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/create_film.ui", self)
        self.setFixedWidth(261)
        self.save_button.clicked.connect(self.create_film)
        self.create_genres_box()
        self.start_time_edit.setDisplayFormat("yyyy MM dd hh mm")

    def create_genres_box(self) -> None:
        genres = cursor.execute("SELECT name FROM genres ORDER BY name").fetchall()
        self.genre_combo_box.addItems([item[0] for item in genres])

    def clear_form(self) -> None:
        self.feedback_label.clear()
        self.name_edit.clear()
        self.duration_box.setValue(0)
        self.room_id_box.setValue(0)
        self.cinema_id_box.setValue(0)
        self.price_box.setValue(0)

    @staticmethod
    def check_film(room: int, start_time: str, film_duration: int) -> bool:
        start_time = dt.datetime(*map(int, start_time.split()))
        if start_time < dt.datetime.now() + dt.timedelta(days=5):
            return False

        all_times = cursor.execute(f"SELECT datetime, duration FROM films WHERE room={room}").fetchall()
        for item in all_times:
            time, duration = item
            item_start_time = dt.datetime(*map(int, time.split()))
            item_end_time = item_start_time + dt.timedelta(minutes=(25 + duration))
            end_time = start_time + dt.timedelta(minutes=(25 + film_duration))
            if end_time < item_start_time and start_time > item_end_time:
                print(item)
                return False

        return True

    @staticmethod
    def insert_seats(seats: int, film_id: int, room_id: int) -> None:
        query = "INSERT INTO seats(taken, room, film) VALUES"
        for _ in range(seats + 1):
            query += f" (0, {room_id}, {film_id}), "
        cursor.execute(query[:-2])

    def create_film(self) -> None:
        self.feedback_label.setText("")
        name = self.name_edit.text()
        genre = self.genre_combo_box.currentText()
        duration = self.duration_box.value()
        start_time = self.start_time_edit.dateTime().toString(self.start_time_edit.displayFormat())
        room_id = self.room_id_box.value()
        cinema_id = self.cinema_id_box.value()
        price = self.price_box.value()

        if name and duration and room_id and cinema_id and self.check_film(room_id, start_time, duration):
            genre_id = cursor.execute(f"SELECT id FROM genres WHERE name='{genre}'").fetchone()[0]
            rows_and_cols = cursor.execute(f"SELECT rows, cols FROM rooms WHERE id={room_id}").fetchone()
            rows_cnt, cols_cnt = rows_and_cols

            film_id = cursor.execute(f"INSERT INTO films (name, genre, duration, datetime, room, "
                                     f"cinema, price, can_buy) "
                                     f"VALUES(?, {genre_id}, {duration}, "
                                     f"?, {room_id}, {cinema_id}, {price}, 1) RETURNING id",
                                     (name, start_time)).fetchone()[0]
            self.insert_seats(rows_cnt * cols_cnt, film_id, room_id)

            connection.commit()
            all_films.load_film_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateGenre(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/create_genre_or_cinema.ui", self)
        self.save_button.clicked.connect(self.define_action)
        self.editing = False
        self.id = None

    def clear_form(self) -> None:
        self.name_edit.clear()
        self.feedback_label.clear()

    def define_action(self) -> None:
        if self.editing:
            self.update_genre()
            self.editing = False
        else:
            self.create_genre()

    def update_genre(self) -> None:
        self.feedback_label.setText("")
        title = self.name_edit.text()

        if title:
            cursor.execute(f"UPDATE genres SET name = ? "           
                           f"WHERE id={self.id}", (title, ))
            connection.commit()
            all_genres.load_genre_data()
            create_film.create_genres_box()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def create_genre(self) -> None:
        self.feedback_label.setText("")
        title = self.name_edit.text()

        if title:
            cursor.execute(f"INSERT INTO genres(name) "
                           f"VALUES (?)", (title, ))
            connection.commit()
            all_genres.load_genre_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def fill_data(self, title: str) -> None:
        self.name_edit.setText(title)

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateCinema(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/create_genre_or_cinema.ui", self)
        self.setWindowTitle("Добавление кинотеатра")
        self.save_button.clicked.connect(self.create_cinema)

    def clear_form(self) -> None:
        self.name_edit.clear()
        self.feedback_label.clear()

    def create_cinema(self) -> None:
        name = self.name_edit.text()
        if name:
            cursor.execute(f"INSERT INTO cinemas(name) "
                           f"VALUES (?)", (name, ))
            connection.commit()
            all_cinemas.load_cinema_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateRoom(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/create_room.ui", self)
        self.setWindowTitle("Добавление кинозала")
        self.save_button.clicked.connect(self.create_room)

    def clear_form(self) -> None:
        self.rows_box.setValue(0)
        self.cols_box.setValue(0)
        self.feedback_label.clear()
        self.cinema_box.setValue(0)

    def create_room(self) -> None:
        rows_cnt = self.rows_box.value()
        cols_cnt = self.cols_box.value()
        cinema_id = self.cinema_box.value()
        cinema = cursor.execute(f"SELECT id from cinemas WHERE id={cinema_id}").fetchall()
        if cols_cnt and cinema_id and len(cinema) and rows_cnt:
            cursor.execute(f"INSERT INTO rooms(cinema, rows, cols) "
                           f"VALUES ({cinema_id}, {rows_cnt}, {cols_cnt})")
            connection.commit()
            all_rooms.load_rooms_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateAfisha(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/create_afisha.ui", self)
        self.setWindowTitle("Создание афиши")
        self.filename = None
        self.genre_id, self.film_name = None, None
        self.save_button.clicked.connect(self.create_afisha)
        self.load_img_button.clicked.connect(self.choose_img)

    def clear_form(self) -> None:
        self.description_edit.clear()
        self.filename = None

    def check_filename(self) -> str:
        if not self.filename.find('data/afisha_images/' + self.filename[self.filename.rfind('/') + 1:]):
            new_fname = 'data/afisha_images/' + self.filename[self.filename.rfind('/') + 1:]
            shutil.copyfile(self.filename, new_fname)
            return new_fname
        return 'data/afisha_images/' + self.filename[self.filename.rfind('/') + 1:]

    def create_afisha(self) -> None:
        description = self.description_edit.toPlainText()
        if description and self.filename:
            fname = self.check_filename()
            afisha_id = cursor.execute(f"INSERT INTO descriptions(image, description) "
                                       f"VALUES(?, ?) RETURNING id", (fname, description)).fetchone()[0]
            cursor.execute(f"UPDATE films SET afisha={afisha_id} WHERE "
                           f"name=? and genre={self.genre_id}", (self.film_name, ))
            connection.commit()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def choose_img(self) -> None:
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png)')[0]
        self.filename = fname

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateReport(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/create_report.ui", self)
        self.setWindowTitle("Отчет")
        self.initUI()

    def initUI(self):
        self.dir_name = None
        self.save_report_button.clicked.connect(self.create_report_query)
        connection.create_function("CHECK_DATETIME", 1, self.check_data)
        self.base_query = "SELECT films.price, films.datetime " \
                          "FROM films " \
                          "INNER JOIN cheques ON cheques.film=films.id " \
                          "WHERE CHECK_DATETIME(films.datetime) = 1 "
        self.create_months_dicts()

    def create_months_dicts(self) -> None:
        self.num_to_month = {1: "Январь", 2: "Февраль", 3: "Март",
                             4: "Апрель", 5: "Май", 6: "Июнь",
                             7: "Июль", 8: "Август", 9: "Сентябрь",
                             10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
        self.month_with_sums = defaultdict(lambda: 0)

    @staticmethod
    def check_data(datetime: str) -> int:
        """
        cheches if film's year is equal to current year
        """
        if dt.datetime(*map(int, datetime.split())).year == dt.datetime.now().year:
            return 1
        return 0

    def create_report_query(self) -> None:
        cinemas = self.cinema_labels.text().lower()
        query = self.base_query
        query_true = False

        if cinemas != "все":
            try:
                cinemas = list(map(int, cinemas.split()))
            except Exception as e:
                self.feedback_label.setText("Неверно заполнена форма")
                return
            query = self.base_query + 'and films.cinema IN (' + ', '.join([str(i) for i in cinemas]) + ')'
            query_true = True
        if cinemas != "все" and not query_true:
            self.feedback_label.setText("Неверно заполнена форма")
            return

        query_result = cursor.execute(query).fetchall()
        self.create_report(query_result)
        self.close()

    def create_report(self, query_result: list) -> None:
        for price, datetime in query_result:
            month = dt.datetime(*map(int, datetime.split())).month
            self.month_with_sums[self.num_to_month[month]] += price

        if not any(self.month_with_sums.values()):
            QMessageBox.warning(self, "Отчет", "Покупок в этом кинотеатре не было",
                                QMessageBox.Ok)
            return

        self.create_csv_table()
        self.create_circle_graphic()
        self.create_months_dicts()
        QMessageBox.warning(self, "Отчет", f"Отчет находится в: {self.dir_name}",
                            QMessageBox.Ok)

    def create_csv_table(self) -> None:
        self.dir_name = 'data/reports/report_' + dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%SS") + '/'
        os.makedirs(self.dir_name)
        with open(self.dir_name + 'table.csv', "w", newline='', encoding="utf-8") as report_csv:
            writer = csv.writer(report_csv, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Месяц", "Доход"])
            for month in self.num_to_month.values():
                row = [month, self.month_with_sums[month]]
                writer.writerow(row)

    def create_circle_graphic(self) -> None:
        labels = [month for month in self.num_to_month.values() if self.month_with_sums[month]]
        values = [self.month_with_sums[month] for month in labels]
        figure, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.axis("equal")
        ax.legend(loc='upper left', bbox_to_anchor=(0.87, 1.0))
        plt.savefig(self.dir_name + 'graphic.png')


class RoomView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/room_with_places.ui", self)
        self.buy_button.clicked.connect(self.buy_seat)
        self.film_id, self.price = 0, 0
        self.cur_row, self.cur_col = -1, -1
        self.user_id = 0
        self.first_seat_id = 0
        self.rows, self.cols = 0, 0

    def fill(self, film_id: int, price: int) -> None:
        self.user_id = int(user_profile.user_id_edit.text())
        self.film_id, self.price = film_id, price
        query_result = cursor.execute("SELECT seats.id, seats.taken, rooms.id, rooms.rows, rooms.cols "
                                      "FROM seats "
                                      "INNER JOIN rooms ON rooms.id = seats.room "
                                      f"WHERE seats.film = {self.film_id}").fetchall()

        self.setWindowTitle(f"Зал {query_result[0][2]}")
        self.first_seat_id = query_result[0][0]
        self.rows, self.cols = query_result[0][3:]

        for row_ind in range(self.rows):
            for col_ind in range(self.cols):
                button = QPushButton(self)
                if not query_result[row_ind * self.cols + col_ind][1]:
                    button.setStyleSheet("background-color: green")
                    button.setText(f"{row_ind + 1}   {self.cols - col_ind}")
                    button.clicked.connect(self.take_seat)
                else:
                    button.setStyleSheet("background-color: red")
                self.seats_grid.addWidget(button, row_ind, col_ind)

    def take_seat(self) -> None:
        self.cur_row, self.cur_col = map(int, self.sender().text().split())
        self.row_edit.setText(str(self.cur_row))
        self.col_edit.setText(str(self.cur_col))

    def buy_seat(self) -> None:
        if self.cur_row >= 0 and self.cur_col >= 0:
            valid = QMessageBox.question(self, "Билет",
                                         "Действительно купить этот билет?",
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                cursor.execute(f"UPDATE users SET total=total+{self.price} WHERE "
                               f"id={self.user_id}")
                cursor.execute("UPDATE seats SET taken=1 WHERE "
                               f"id={self.first_seat_id + (self.cur_row - 1) * self.cols + (self.cols - self.cur_col)}")
                unique_cheque_key = self.generate_random_key()
                cheque_id = cursor.execute("INSERT INTO cheques(key, user, film) "
                                           f"VALUES('{unique_cheque_key}', {self.user_id}, "
                                           f"{self.film_id}) RETURNING id").fetchone()[0]
                connection.commit()
                user_profile.load_cheques_data(self.user_id)
                self.create_text_cheque(cheque_id,
                                        dt.datetime.now().strftime("%Y.%m.%d %H:%M"),
                                        unique_cheque_key)
                self.close()

    def create_text_cheque(self, cheque_id: int, datetime: str, unique_cheque_key: str) -> None:
        """
        creates cheques to user's purchase
        """
        cheque_path = f"data/cheques/cheque_{cheque_id}"

        with open(cheque_path, "w", encoding="utf-8") as cheque:
            cheque.write("Чек\n---------------------------------------\n"
                         f"ID фильма: {self.film_id}\n"
                         f"Время покупки: {datetime}\n"
                         f"Номер чека: {cheque_id}\n"
                         f"Уникальный ID чека: {unique_cheque_key}\n"
                         f"Ряд: {self.cur_row}, место: {self.cur_col}\n"
                         f"---------------------------------------\n"
                         f"Спасибо за покупку!")

            QMessageBox.warning(self, "Чек",
                                f"Чек сохранен в файле: {cheque_path}",
                                QMessageBox.Ok)

    @staticmethod
    def generate_random_key() -> str:
        chars = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        result = ''.join([choice(chars) for _ in range(10)])
        return result

    def clear_form(self) -> None:
        self.row_edit.setText("")
        self.col_edit.setText("")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear_form()


class AfishaView(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/film_afisha.ui", self)

    def fill(self, name: str, genre: str, description: str, image: str) -> None:
        self.setWindowTitle(name)
        self.img = QPixmap(image)
        self.img = self.img.scaledToWidth(461)
        self.img = self.img.scaledToHeight(281)
        self.pic_label.setPixmap(self.img)
        self.name_label.setText(name)
        self.description_label.setText(description)
        self.description_label.adjustSize()
        self.genre_label.setText(genre)


class UserFilms(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/user_films.ui", self)
        self.initUI()

    def initUI(self) -> None:
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

    def search(self) -> None:
        search_by = self.search_by_box.currentText()
        search_text = self.search_edit.text()

        if search_by == 'Нет':
            self.query = self.base_query[:]

        if search_text:
            if search_by == "Кинотеатр":
                self.query = self.base_query + f" WHERE cinemas.name LIKE '%{search_text}%'"
            elif search_by == "Название":
                self.query = self.base_query + f" WHERE films.name LIKE '%{search_text}%'"
            elif search_by == "Жанр":
                self.query = self.base_query + f" WHERE genres.name LIKE '%{search_text}%'"
            elif search_by == "Максимальная цена" and search_text.isdigit():
                self.query = self.base_query + f" WHERE films.price <= {int(search_text)}"
            self.load_films_data()

    def load_films_data(self) -> None:
        query_result = cursor.execute(self.query + self.order).fetchall()

        if query_result:
            titles = ["ИД", "Название фильма", "Жанр", "Продолжительность", "Начало", "Кинотеатр", "Зал", "Цена"]
            create_table(titles, query_result, self.films_table_data)
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
            afisha_view.fill(*afisha)
            afisha_view.show()
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

        self.room.fill(film_id, price)
        self.room.show()

    def clear_table(self) -> None:
        while self.films_table_data.rowCount():
            self.films_table_data.removeRow(0)


class UserProfile(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/user_profile.ui", self)

    def fill(self, user_id: int) -> None:
        user_data = cursor.execute(f"SELECT username, total FROM users WHERE id={user_id}").fetchone()
        self.user_id_edit.setText(str(user_id))
        self.username_edit.setText(user_data[0])
        self.total_money_edit.setText(str(user_data[1]))
        self.load_cheques_data(user_id)

    def load_cheques_data(self, user_id):
        query_result = cursor.execute(f"SELECT "
                                      f"cheques.id, cheques.key, films.name, films.datetime "
                                      f"FROM cheques "
                                      f"INNER JOIN films ON films.id = cheques.film "
                                      f"WHERE cheques.user = {user_id}"
                                      ).fetchall()

        if query_result:
            titles = ["ID", "Ключ", "Название фильма", "Начало фильма"]
            create_table(titles, query_result, self.purchase_table_data, enable=True)


class AllFilms(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/films.ui", self)
        self.setFixedWidth(710)
        self.create_afisha_form = CreateAfisha()
        self.initUI()

    def initUI(self) -> None:
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
                                         "У данного фильма уже есть афиша, удалить и перезаписать?",
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
            titles = ["ИД", "Название фильма", "Жанр", "Продолжительность", "Начало", "Кинотеатр", "Зал", "Цена"]
            create_table(titles, query_result, self.film_table_data)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.film_table_data.rowCount() > 0:
            self.film_table_data.removeRow(0)

    @staticmethod
    def add_film() -> None:
        create_film.setWindowTitle("Добавление фильма")
        create_film.show()

    def delete_film(self) -> None:
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный фильм?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            film_id = int(self.film_table_data.item(row, 0).text())
            cursor.executescript(f"UPDATE films SET can_buy = 0 WHERE id={film_id}; "
                                 f"DELETE FROM seats WHERE film={film_id}")
            connection.commit()
            self.load_film_data()


class AllGenres(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/genres.ui", self)
        self.create_genre = CreateGenre()
        self.setFixedWidth(710)
        self.initUI()

    def initUI(self) -> None:
        self.add_genre_button.clicked.connect(self.add_genre)
        self.edit_genre_button.clicked.connect(self.change_genre)
        self.delete_genre_button.clicked.connect(self.delete_genre)
        self.load_genre_data()

    def load_genre_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM GENRES").fetchall()

        if query_result:
            titles = ["ИД", "Название жанра"]
            create_table(titles, query_result, self.genre_table_data)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.genre_table_data.rowCount() > 0:
            self.genre_table_data.removeRow(0)

    def add_genre(self) -> None:
        self.create_genre.setWindowTitle("Добавление жанра")
        self.create_genre.show()

    def change_genre(self) -> None:
        row = self.genre_table_data.currentRow()

        if row >= 0:
            title = self.genre_table_data.item(row, 1).text()
            self.create_genre.fill_data(title)
            self.create_genre.editing = True
            self.create_genre.id = int(self.genre_table_data.item(row, 0).text())
            self.create_genre.setWindowTitle("Изменение жанра")
            self.create_genre.show()

    def delete_genre(self) -> None:
        row = self.genre_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный жанр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            genre_id = int(self.genre_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE genre={genre_id}; "
                                 f"DELETE FROM genres WHERE id={genre_id}")
            connection.commit()
            self.load_genre_data()
            all_films.load_film_data()


class AllCinemas(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/cinemas.ui", self)
        self.create_cinema = CreateCinema()
        self.report = CreateReport()
        self.setFixedWidth(711)
        self.initUI()

    def initUI(self) -> None:
        self.add_cinema_button.clicked.connect(self.add_cinema)
        self.delete_cinema_button.clicked.connect(self.delete_cinema)
        self.report_button.clicked.connect(self.create_report)
        self.load_cinema_data()

    def create_report(self):
        self.report.show()

    def load_cinema_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM cinemas").fetchall()

        if query_result:
            titles = ["ID", "Имя"]
            create_table(titles, query_result, self.cinema_table_data)
        else:
            self.clear_table()

    def add_cinema(self) -> None:
        self.create_cinema.show()

    def clear_table(self) -> None:
        while self.cinema_table_data.rowCount() > 0:
            self.cinema_table_data.removeRow(0)

    def delete_cinema(self) -> None:
        row = self.cinema_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный кинотеатр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cinema_id = int(self.cinema_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE cinema={cinema_id}; "
                                 f"DELETE FROM rooms WHERE cinema={cinema_id}; "
                                 f"DELETE FROM cinemas WHERE id={cinema_id}")
            connection.commit()
            self.load_cinema_data()
            all_films.load_film_data()
            all_rooms.load_rooms_data()


class AllRooms(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/rooms.ui", self)
        self.create_room = CreateRoom()
        self.setFixedWidth(711)
        self.initUI()

    def initUI(self) -> None:
        self.add_room_button.clicked.connect(self.add_room)
        self.delete_room_button.clicked.connect(self.delete_room)
        self.load_rooms_data()

    def load_rooms_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM rooms").fetchall()

        if query_result:
            titles = ["ID", "ID кинотеатра", "Число рядов", "Число мест в ряду"]
            create_table(titles, query_result, self.room_table_data)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.room_table_data.rowCount() > 0:
            self.room_table_data.removeRow(0)

    def add_room(self) -> None:
        self.create_room.show()

    def delete_room(self) -> None:
        row = self.room_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный зал?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            room_id = int(self.room_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE room={room_id}; "
                                 f"DELETE FROM seats WHERE room={room_id}; "
                                 f"DELETE FROM rooms WHERE id={room_id}")
            connection.commit()
            self.load_rooms_data()
            all_films.load_film_data()


class AllUsers(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("data/ui/users.ui", self)
        self.load_users_data()

    def load_users_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM users").fetchall()
        titles = ["ID", "Имя", "Пароль", "Админ", "Сумма покупок"]
        create_table(titles, query_result, self.users_table_data, enable=True)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    user_profile, all_cinemas = None, None
    all_films, all_genres = None, None
    all_rooms, create_film = None, None
    main_admin_window, user_main_window = None, None
    afisha_view, user_films = None, None
    login_window = LoginWindow()
    register_window = RegisterWindow()
    login_window.show()
    sys.exit(app.exec_())
