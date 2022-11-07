import csv
import os
import shutil
import sys
from collections import defaultdict
from random import choice
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import hashlib
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QMessageBox,
                             QTableWidgetItem, QHeaderView, QFileDialog,
                             QMenu, QMenuBar, QAction, QTableWidget, QPushButton, QInputDialog)
from data.py_files.ui_code import *


connection = sqlite3.connect("data/CinemaSystemDatabase.db")
cursor = connection.cursor()


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def create_table(titles: list, query_result: list, table: QTableWidget, equal_cols: bool = True,
                 need_datetime=False, column=-1) -> None:
    """
    fills table with taken column titles,
    using data from query_result
    """
    table.setRowCount(len(query_result))
    table.setColumnCount(len(query_result[0]))
    table.setHorizontalHeaderLabels(titles)

    for i, elem in enumerate(query_result):
        for j, val in enumerate(elem):
            table.setItem(i, j, QTableWidgetItem(str(val)))

    table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # set table read only
    if equal_cols:
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # to set columns equal width
    if need_datetime:
        format_datetime(table, column)


def format_datetime(table: QTableWidget, column: int):
    """
    format datetime in tables
    """
    for row in range(table.rowCount()):
        datetime = table.item(row, column).text()
        formated_datetime = dt.datetime(*map(int, datetime.split())).strftime("%d.%m.%Y %H:%M")
        table.item(row, column).setText(formated_datetime)


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menubar()
        self.cur_main_window = None
        self.login_window = LoginWindow()
        self.register_window = RegisterWindow()
        self.login_window.show()

    def create_menubar(self) -> None:
        self.menuBar = QMenuBar(self)
        self.menu = QMenu("Меню", self)
        self.login_action = QAction("Смена пользователя", self)
        self.menuBar.addMenu(self.menu)
        self.menu.addAction(self.login_action)
        self.login_action.triggered.connect(self.change_user)
        self.setMenuBar(self.menuBar)

    def change_user(self) -> None:
        self.login_window.show()
        self.close()


class AdminMainWindow(BaseWindow, Ui_AdminMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(710)
        self.create_tab_widget()
        self.login_window.close()

    def create_tab_widget(self) -> None:
        self.all_cinemas = AllCinemas()
        self.all_rooms = AllRooms()
        self.all_films = AllFilms()
        self.all_genres = AllGenres()
        self.all_users = AllUsers()
        self.all_reports = AllReports()
        self.tabWidget.addTab(self.all_cinemas, "Кинотеатры")
        self.tabWidget.addTab(self.all_rooms, "Залы")
        self.tabWidget.addTab(self.all_films, "Сеансы")
        self.tabWidget.addTab(self.all_genres, "Жанры")
        self.tabWidget.addTab(self.all_users, "Пользователи")
        self.tabWidget.addTab(self.all_reports, "Отчеты")


class UserMainWindow(BaseWindow, Ui_UserMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_tab_widget()
        self.login_window.close()

    def create_tab_widget(self) -> None:
        self.user_films = UserFilms()
        self.user_profile = UserProfile()
        self.tabWidget.addTab(self.user_films, "Сеансы")
        self.tabWidget.addTab(self.user_profile, "Мой профиль")


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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

        password_text = hashlib.sha256(password_text.encode('utf-8')).hexdigest()
        user_obj = cursor.execute(f"SELECT id, admin FROM users WHERE username = ?"
                                  f" and password='{password_text}'", (login_text, )).fetchone()
        if user_obj:
            user_id, is_admin = user_obj
            if is_admin:
                base_window.cur_main_window = AdminMainWindow()
            else:
                base_window.cur_main_window = UserMainWindow()
                base_window.cur_main_window.user_profile.fill(user_id)
            base_window.cur_main_window.show()
            self.clear_and_close()
        else:
            QMessageBox.critical(
                self, 'Ошибка входа', "Неправильный логин или пароль",
                QMessageBox.Ok)
            return

    def register(self) -> None:
        self.clear_and_close()
        base_window.register_window.show()

    def clear_and_close(self) -> None:
        self.login_edit.clear()
        self.password_edit.clear()
        self.close()


class RegisterWindow(QWidget, Ui_Register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.setFixedSize(307, 213)
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self) -> None:
        base_window.login_window.show()
        self.clear_and_close()

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
                self, 'Ошибка регистрации', "Такой пользователь уже существует",
                QMessageBox.Ok)
            return

        password_text = hashlib.sha256(password_text.encode('utf-8')).hexdigest()
        cursor.execute(f"INSERT INTO USERS(username, password, admin) "
                       f"VALUES(?, ?, 0)",
                       (login_text, password_text))
        QMessageBox.information(
            self, 'Успех', "Успешно создание пользователя!",
            QMessageBox.Ok)
        connection.commit()
        self.clear()

    def clear_and_close(self) -> None:
        self.login_edit.clear()
        self.password_edit.clear()
        self.password_again.clear()
        self.close()


class CreateFilm(QWidget, Ui_CreateFilm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(261, 312)
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
        end_time = start_time + dt.timedelta(minutes=(25 + film_duration))
        if start_time < dt.datetime.now() + dt.timedelta(days=5):
            return False

        all_times = cursor.execute(f"SELECT datetime, duration FROM films WHERE room={room}").fetchall()
        for item in all_times:
            time, duration = item
            item_start_time = dt.datetime(*map(int, time.split()))
            item_end_time = item_start_time + dt.timedelta(minutes=(25 + duration))
            if item_start_time <= start_time < item_end_time or item_start_time < end_time <= item_end_time:
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
        room_in_cinema = cursor.execute("SELECT id FROM rooms WHERE id=? and cinema=?",
                                        (room_id, cinema_id)).fetchone()

        if name and duration and room_id and cinema_id and room_in_cinema and self.check_film(room_id, start_time,
                                                                                              duration):
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
            base_window.cur_main_window.all_films.load_film_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateRoom(QWidget, Ui_CreateRoom):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(345, 131)
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
            base_window.cur_main_window.all_rooms.load_rooms_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateAfisha(QWidget, Ui_CreateAfisha):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(236, 211)
        self.filename = None
        self.genre_id, self.film_name = None, None
        self.save_button.clicked.connect(self.create_afisha)
        self.load_img_button.clicked.connect(self.choose_img)

    def clear_form(self) -> None:
        self.description_edit.clear()
        self.filename = None

    def check_filename(self) -> str:
        new_fname = 'data/afisha_images/' + self.filename[self.filename.rfind('/') + 1:]
        if not os.path.isfile(new_fname):
            shutil.copyfile(self.filename, new_fname)
        return new_fname

    def create_afisha(self) -> None:
        description = self.description_edit.toPlainText()
        if description and self.filename:
            fname = self.check_filename()
            afisha_id = cursor.execute("INSERT INTO descriptions(image, description) "
                                       "VALUES(?, ?) RETURNING id", (fname, description)).fetchone()[0]
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


class CreateReport(QWidget, Ui_CreateReport):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(241, 130)
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
            except Exception:
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
            QMessageBox.warning(self, "Отчет", "За этот год покупок не было",
                                QMessageBox.Ok)
            return

        datetime = self.create_csv_table()
        self.create_circle_graphic()
        self.create_months_dicts()
        QMessageBox.warning(self, "Отчет", f"Отчет находится в: {self.dir_name}",
                            QMessageBox.Ok)
        cursor.execute("INSERT INTO reports(path, datetime) VALUES(?, ?)", (self.dir_name, datetime))
        connection.commit()
        base_window.cur_main_window.all_reports.load_report_data()

    def create_csv_table(self) -> str:
        datetime = dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.dir_name = 'data/reports/report_' + datetime + '/'
        os.makedirs(self.dir_name)
        with open(self.dir_name + 'table.csv', "w", newline='', encoding="utf-8") as report_csv:
            writer = csv.writer(report_csv, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Месяц", "Доход"])
            for month in self.num_to_month.values():
                row = [month, self.month_with_sums[month]]
                writer.writerow(row)
        return datetime

    def create_circle_graphic(self) -> None:
        labels = [month for month in self.num_to_month.values() if self.month_with_sums[month]]
        values = [self.month_with_sums[month] for month in labels]
        figure, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.axis("equal")
        ax.legend(loc='upper left', bbox_to_anchor=(0.87, 1.0))
        plt.savefig(self.dir_name + 'graphic.png')


class RoomView(QWidget, Ui_RoomView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buy_button.clicked.connect(self.buy_seat)
        self.film_id, self.price = 0, 0
        self.cur_row, self.cur_col = -1, -1
        self.user_id = 0
        self.first_seat_id = 0
        self.rows, self.cols = 0, 0

    def fill(self, film_id: int, price: int) -> None:
        self.user_id = int(base_window.cur_main_window.user_profile.user_id_edit.text())
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
                base_window.cur_main_window.user_profile.load_cheques_data(self.user_id)
                base_window.cur_main_window.user_profile.total_money_edit.setText(str(int(base_window.cur_main_window.
                                                                                          user_profile.total_money_edit.
                                                                                          text())
                                                                                      + self.price))
                self.create_text_cheque(cheque_id,
                                        dt.datetime.now().strftime("%d.%m.%Y %H:%M"),
                                        unique_cheque_key)
                self.close()

    def create_text_cheque(self, cheque_id: int, datetime: str, unique_cheque_key: str) -> None:
        """
        creates cheques to user's purchase
        """
        cheque_path = f"data/cheques/cheque_{cheque_id}"

        film_data = cursor.execute("SELECT films.name, cinemas.name, films.room, films.datetime, films.price "
                                   "FROM films "
                                   "INNER JOIN cinemas ON films.cinema=cinemas.id "
                                   f"WHERE films.id={self.film_id}").fetchone()

        with open(cheque_path, "w", encoding="utf-8") as cheque:
            cheque.write("Чек\n---------------------------------------\n"
                         f"Название фильма: {film_data[0]}\n"
                         f"Название кинотеатра: {film_data[1]}\n"
                         f"ID зала: {film_data[2]}\n"
                         f"Начало фильма: {dt.datetime(*map(int, film_data[3].split())).strftime('%d.%m.%Y %H:%M')}\n"
                         f"Номер чека: {cheque_id}\n"
                         f"Уникальный ключ: {unique_cheque_key}\n"
                         f"Время покупки: {datetime}\n"
                         f"Ряд: {self.cur_row}, место: {self.cur_col}\n"
                         f"Сумма покупки: {film_data[4]}\n"
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
        self.cur_row, self.cur_col = -1, -1
        while self.seats_grid.count():
            child = self.seats_grid.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear_form()


class AfishaView(QWidget, Ui_AfishaView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(480)

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


class ChequeView(QWidget, Ui_ChequeView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(322, 362)

    def fill(self, filename: str):
        if not os.path.isfile(filename):
            QMessageBox.critical(self, "Чек", "Файл не найден",
                                 QMessageBox.Ok)
            return

        with open(filename, encoding="utf-8") as cheque:
            data = cheque.readlines()
            self.film_name_edit.setText(data[2][data[2].find(': ') + 2:])
            self.cinema_name_edit.setText(data[3][data[3].find(': ') + 2:])
            self.room_id_edit.setText(data[4][data[4].find(': ') + 2:])
            self.film_start_edit.setText(data[5][data[5].find(': ') + 2:])
            self.cheque_id_edit.setText(data[6][data[6].find(': ') + 2:])
            self.unique_key_edit.setText(data[7][data[7].find(': ') + 2:])
            self.buy_time_edit.setText(data[8][data[8].find(': ') + 2:])
            self.row_edit.setText(data[9][data[9].find(': ') + 2:data[9].find(',')])
            self.col_edit.setText(data[9][data[9].rfind(': ') + 2:])
            self.total_edit.setText(data[10][data[10].find(': ') + 2:])
        self.show()


class ReportView(QWidget, Ui_ReportView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(660, 719)

    def fill(self, dir_name: str) -> None:
        pixmap = QPixmap(dir_name + "/graphic.png")
        self.image.setPixmap(pixmap)
        table_data = list()
        with open(dir_name + 'table.csv', encoding="utf-8") as csvtable:
            reader = csv.reader(csvtable, delimiter=';', quoting=csv.QUOTE_NONE)
            next(reader)
            for row in reader:
                if int(row[1]):
                    table_data.append((row[0], row[1]))
        create_table(["Месяц", "Оборот"], table_data, self.months_table_data)
        self.show()


class UserFilms(QWidget, Ui_UserFilms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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

        self.room.fill(film_id, price)
        self.room.show()

    def clear_table(self) -> None:
        while self.films_table_data.rowCount():
            self.films_table_data.removeRow(0)


class UserProfile(QWidget, Ui_UserProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def fill(self, user_id: int) -> None:
        self.cheque_view = ChequeView()
        user_data = cursor.execute(f"SELECT username, total FROM users WHERE id={user_id}").fetchone()
        self.user_id_edit.setText(str(user_id))
        self.username_edit.setText(user_data[0])
        self.total_money_edit.setText(str(user_data[1]))
        self.watch_cheque_button.clicked.connect(self.watch_cheque)
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
            create_table(titles, query_result, self.purchase_table_data, need_datetime=True, column=3)

    def watch_cheque(self):
        row = self.purchase_table_data.currentRow()
        if row == -1:
            return

        filename = 'data/cheques/cheque_' + self.purchase_table_data.item(row, 0).text()
        self.cheque_view.fill(filename)


class AllFilms(QWidget, Ui_AllFilms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_film = CreateFilm()
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


class AllGenres(QWidget, Ui_AllGenres):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
        name, ok_pressed = QInputDialog.getText(self, "Жанр",
                                                "Введите имя нового жанра")
        if ok_pressed:
            if name:
                cursor.execute(f"INSERT INTO genres(name) "
                               f"VALUES (?)", (name,))
                connection.commit()
                self.load_genre_data()
                base_window.cur_main_window.all_films.create_film.create_genres_box()
            else:
                QMessageBox.critical(self, "Ошибка",
                                     "Неверно заполнена форма")

    def change_genre(self) -> None:
        row = self.genre_table_data.currentRow()

        if row >= 0:
            name, ok_pressed = QInputDialog.getText(self, "Жанр",
                                                    "Введите имя нового жанра")
            if ok_pressed:
                if name:
                    cursor.execute(f"UPDATE genres SET name=? "
                                   f"WHERE id=?", (name, int(self.genre_table_data.item(row, 0).text())))
                    connection.commit()
                    self.load_genre_data()
                    base_window.cur_main_window.all_films.create_film.create_genres_box()
                else:
                    QMessageBox.critical(self, "Ошибка",
                                         "Неверно заполнена форма")

    def delete_genre(self) -> None:
        row = self.genre_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, 'Удаление жанра', "Действительно удалить данный жанр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            genre_id = int(self.genre_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE genre={genre_id}; "
                                 f"DELETE FROM genres WHERE id={genre_id}")
            connection.commit()
            self.load_genre_data()
            base_window.cur_main_window.all_films.create_film.create_genres_box()


class AllCinemas(QWidget, Ui_AllCinemas):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
        name, ok_pressed = QInputDialog.getText(self, "Кинотеатр",
                                                "Введите имя нового кинотеатра")
        if ok_pressed:
            if name:
                cursor.execute(f"INSERT INTO cinemas(name) "
                               f"VALUES (?)", (name,))
                connection.commit()
                self.load_cinema_data()
            else:
                QMessageBox.critical(self, "Ошибка",
                                     "Неверно заполнена форма")

    def clear_table(self) -> None:
        while self.cinema_table_data.rowCount() > 0:
            self.cinema_table_data.removeRow(0)

    def delete_cinema(self) -> None:
        row = self.cinema_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, 'Удаление кинотеатра', "Действительно удалить данный кинотеатр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cinema_id = int(self.cinema_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE cinema={cinema_id}; "
                                 f"DELETE FROM rooms WHERE cinema={cinema_id}; "
                                 f"DELETE FROM cinemas WHERE id={cinema_id}")
            connection.commit()
            self.load_cinema_data()
            base_window.cur_main_window.all_films.load_film_data()
            base_window.cur_main_window.all_rooms.load_rooms_data()


class AllRooms(QWidget, Ui_AllRooms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_room = CreateRoom()
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
                self, 'Удаление зала', "Действительно удалить данный зал?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            room_id = int(self.room_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE room={room_id}; "
                                 f"DELETE FROM seats WHERE room={room_id}; "
                                 f"DELETE FROM rooms WHERE id={room_id}")
            connection.commit()
            self.load_rooms_data()
            base_window.cur_main_window.all_films.load_film_data()


class AllUsers(QWidget, Ui_AllUsers):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_users_data()

    def load_users_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM users").fetchall()
        titles = ["ID", "Имя", "Пароль", "Админ", "Сумма покупок"]
        create_table(titles, query_result, self.users_table_data)


class AllReports(QWidget, Ui_AllReports):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.report_view = ReportView()
        self.delete_button.clicked.connect(self.delete_report)
        self.watch_button.clicked.connect(self.watch_report)
        self.load_report_data()

    def delete_report(self):
        row = self.reports_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
            self, 'Удаление отчета', "Действительно удалить данный отчет?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            report_id = self.reports_table_data.item(row, 0).text()
            report_path = self.reports_table_data.item(row, 1).text()
            cursor.execute(f"DELETE FROM reports WHERE id={report_id}")
            connection.commit()
            shutil.rmtree(report_path)
            self.load_report_data()

    def watch_report(self):
        row = self.reports_table_data.currentRow()
        if row == -1:
            return

        dir_name = self.reports_table_data.item(row, 1).text()
        if not os.path.isdir(dir_name):
            QMessageBox.critical(self, "Отчет", "Файл не найден",
                                 QMessageBox.Ok)
            return
        self.report_view.fill(dir_name)

    def load_report_data(self):
        query_result = cursor.execute("SELECT * FROM reports").fetchall()
        if query_result:
            titles = ["ID", "Путь к файлу", "Время создания"]
            create_table(titles, query_result, self.reports_table_data, equal_cols=False)
            self.reports_table_data.setColumnWidth(0, 30)
            self.reports_table_data.setColumnWidth(1, 317)
            self.reports_table_data.setColumnWidth(2, 318)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    base_window = BaseWindow()
    sys.exit(app.exec_())
