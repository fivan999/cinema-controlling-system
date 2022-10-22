import shutil
import sys
from PyQt5 import uic
import datetime as dt
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QMessageBox,
                             QTableWidgetItem, QHeaderView, QFileDialog,
                             QMenu, QMenuBar, QAction)
import sqlite3


connection = sqlite3.connect("CinemaSystemDatabase.db")
cursor = connection.cursor()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def create_menubar(self):
        self.menuBar = QMenuBar(self)
        self.menu = QMenu("Меню", self)
        self.login_action = QAction("Смена пользователя", self)
        self.menuBar.addMenu(self.menu)
        self.menu.addAction(self.login_action)
        self.login_action.triggered.connect(self.change_user)
        self.setMenuBar(self.menuBar)

    def change_user(self):
        login_window.show()
        self.close()


class AdminMainWindow(MainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("admin_main_window.ui", self)
        self.setFixedWidth(710)
        self.setWindowTitle("Фильмотека")
        self.tabWidget.addTab(all_cinemas, "Кинотеатры")
        self.tabWidget.addTab(all_rooms, "Залы")
        self.tabWidget.addTab(all_films, "Фильмы")
        self.tabWidget.addTab(all_genres, "Жанры")
        self.create_menubar()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("login.ui", self)
        self.setWindowTitle("Вход")
        self.initUI()

    def initUI(self):
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        login_text = self.login_edit.text()
        password_text = self.password_edit.text()

        if not login_text:
            QMessageBox.question(
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин",
                QMessageBox.Ok)
            return
        if not password_text:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль",
                QMessageBox.Ok)
            return

        user_obj = cursor.execute(f"SELECT admin FROM users WHERE username = '{login_text}'"
                                  f" and password = '{password_text}'").fetchall()
        if user_obj:
            is_admin = user_obj[0][0]
            if is_admin:
                self.clear()
                main_admin_window.show()
            else:
                pass
        else:
            QMessageBox.question(
                self, 'Ошибка входа', "Неравильный логин или пароль",
                QMessageBox.Ok)
            return

    def register(self):
        register_window.show()
        self.clear()
        self.close()

    def clear(self):
        self.close()
        self.login_edit.clear()
        self.password_edit.clear()


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("register.ui", self)
        self.setWindowTitle("Регистрация")
        self.initUI()

    def initUI(self):
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        login_window.show()
        self.close()
        self.clear()

    def register(self):
        login_text = self.login_edit.text()
        password_text = self.password_edit.text()
        password_text_again = self.password_again.text()

        if not login_text:
            QMessageBox.question(
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин",
                QMessageBox.Ok)
            return
        if not password_text or not password_text_again:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль и подтвердите его",
                QMessageBox.Ok)
            return
        if password_text != password_text_again:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Пароли не совпадают",
                QMessageBox.Ok)
            return

        user_obj = cursor.execute(f"SELECT username FROM users WHERE username = '{login_text}'").fetchall()
        if user_obj:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Такой пользователь уже существует",
                QMessageBox.Ok)
            return

        cursor.execute(f"INSERT INTO USERS(username, password, admin) "
                       f"VALUES('{login_text}', '{password_text}', 0)")
        QMessageBox.question(
            self, 'Успех', "Успешно создание пользователя!",
            QMessageBox.Ok)
        connection.commit()
        self.clear()

    def clear(self):
        self.login_edit.clear()
        self.password_edit.clear()
        self.password_again.clear()


class CreateFilm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("create_film.ui", self)
        self.setFixedWidth(261)
        self.save_button.clicked.connect(self.create_film)
        self.create_genres_box()
        self.start_time_edit.setDisplayFormat("yyyy MM dd hh mm")

    def create_genres_box(self):
        genres = cursor.execute("SELECT name FROM genres ORDER BY name").fetchall()
        self.genre_combo_box.addItems([item[0] for item in genres])

    def clear_form(self):
        self.feedback_label.clear()
        self.name_edit.clear()
        self.duration_box.setValue(0)
        self.room_id_box.setValue(0)
        self.cinema_id_box.setValue(0)
        self.price_box.setValue(0)

    def check_film(self, room, start_time):
        start_time = dt.datetime(*list(map(int, start_time.split())))
        if start_time < dt.datetime.now() + dt.timedelta(days=5):
            return False

        all_times = cursor.execute(f"SELECT datetime, duration FROM films WHERE room={room}").fetchall()
        for item in all_times:
            time, duration = item
            if start_time < dt.datetime(*list(map(int, time.split()))) + dt.timedelta(minutes=(25 + duration)):
                return False

        return True

    def insert_seats(self, seats, film_id, room_id):
        query = "INSERT INTO seats(taken, room, film) VALUES"
        for _ in range(seats):
            query += f" (0, {room_id}, {film_id}), "
        cursor.execute(query[:-2])

    def create_film(self):
        self.feedback_label.setText("")
        name = self.name_edit.text()
        genre = self.genre_combo_box.currentText()
        duration = self.duration_box.value()
        start_time = self.start_time_edit.dateTime().toString(self.start_time_edit.displayFormat())
        room_id = self.room_id_box.value()
        cinema_id = self.cinema_id_box.value()
        price = self.price_box.value()

        if name and duration and room_id and cinema_id and self.check_film(room_id, start_time):
            genre_id = cursor.execute(f"SELECT id FROM genres WHERE name='{genre}'").fetchone()[0]
            rows_and_cols = cursor.execute(f"SELECT rows, cols FROM rooms WHERE id={room_id}").fetchone()
            rows_cnt, cols_cnt = rows_and_cols

            film_id = cursor.execute(f"INSERT INTO films (name, genre, duration, datetime, room, cinema, price) "
                                     f"VALUES('{name}', {genre_id}, {duration}, "
                                     f"'{start_time}', {room_id}, {cinema_id}, {price}) RETURNING id").fetchone()[0]
            self.insert_seats(rows_cnt * cols_cnt, film_id, room_id)

            connection.commit()
            all_films.load_film_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event):
        self.clear_form()


class CreateGenre(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("create_genre_or_cinema.ui", self)
        self.save_button.clicked.connect(self.define_action)
        self.editing = False
        self.id = None

    def clear_form(self):
        self.name_edit.clear()
        self.feedback_label.clear()

    def define_action(self):
        if self.editing:
            self.update_genre()
            self.editing = False
        else:
            self.create_genre()

    def update_genre(self):
        self.feedback_label.setText("")
        title = self.name_edit.text()

        if title:
            cursor.execute(f"UPDATE genres SET name = '{title}' "           
                           f"WHERE id={self.id}")
            connection.commit()
            all_genres.load_genre_data()
            create_film.create_genres_box()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def create_genre(self):
        self.feedback_label.setText("")
        title = self.name_edit.text()

        if title:
            cursor.execute(f"INSERT INTO genres(name) "
                           f"VALUES ('{title}')")
            connection.commit()
            all_genres.load_genre_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def fill_data(self, title):
        self.name_edit.setText(title)

    def closeEvent(self, event):
        self.clear_form()


class CreateCinema(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("create_genre_or_cinema.ui", self)
        self.setWindowTitle("Добавление кинотеатра")
        self.save_button.clicked.connect(self.create_cinema)

    def clear_form(self):
        self.name_edit.clear()
        self.feedback_label.clear()

    def create_cinema(self):
        name = self.name_edit.text()
        if name:
            cursor.execute(f"INSERT INTO cinemas(name) "
                           f"VALUES ('{name}')")
            connection.commit()
            all_cinemas.load_cinema_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event):
        self.clear_form()


class CreateRoom(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("create_room.ui", self)
        self.setWindowTitle("Добавление кинозала")
        self.save_button.clicked.connect(self.create_room)

    def clear_form(self):
        self.rows_box.setValue(0)
        self.cols_box.setValue(0)
        self.feedback_label.clear()
        self.cinema_box.setValue(0)

    def create_room(self):
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

    def closeEvent(self, event):
        self.clear_form()


class CreateAfisha(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("create_afisha.ui", self)
        self.setWindowTitle("Создание афиши")
        self.filename = None
        self.genre_id, self.film_name = None, None
        self.save_button.clicked.connect(self.create_afisha)
        self.load_img_button.clicked.connect(self.choose_img)

    def clear_form(self):
        self.description_edit.clear()
        self.filename = None

    def check_filename(self):
        if 'afisha_images/' + self.filename[self.filename.find('/') + 1:] != self.filename:
            new_fname = 'afisha_images/' + self.filename[self.filename.rfind('/') + 1:]
            shutil.copyfile(self.filename, new_fname)
            return new_fname
        return self.filename

    def create_afisha(self):
        description = self.description_edit.toPlainText()
        if description and self.filename:
            fname = self.check_filename()
            afisha_id = cursor.execute(f"INSERT INTO descriptions(image, description) "
                                       f"VALUES('{fname}', '{description}') RETURNING id").fetchone()[0]
            cursor.execute(f"UPDATE films SET afisha={afisha_id} WHERE "
                           f"name='{self.film_name}' and genre={self.genre_id}")
            connection.commit()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def choose_img(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png)')[0]
        self.filename = fname

    def closeEvent(self, event):
        self.clear_form()


class AllFilms(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("films.ui", self)
        self.setFixedWidth(710)
        self.initUI()

    def initUI(self):
        self.add_film_button.clicked.connect(self.add_film)
        self.delete_film_button.clicked.connect(self.delete_film)
        self.create_afisha_button.clicked.connect(self.create_afisha)
        self.load_film_data()

    def create_afisha(self):
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        film_name = self.film_table_data.item(row, 1).text()
        genre_name = self.film_table_data.item(row, 2).text()
        genre_id = cursor.execute(f"SELECT id from genres WHERE name='{genre_name}'").fetchone()[0]
        create_afisha.film_name = film_name
        create_afisha.genre_id = genre_id
        create_afisha.show()

    def load_film_data(self):
        query_result = cursor.execute(f"SELECT "
                                      f"films.id, films.name, genres.name, films.duration, "
                                      f"films.datetime, cinemas.name, rooms.id, films.price "
                                      f"FROM films "
                                      f"INNER JOIN genres ON genres.id = films.genre "
                                      f"INNER JOIN cinemas ON cinemas.id = films.cinema "
                                      f"INNER JOIN rooms ON rooms.id = films.room "
                                      f"ORDER BY films.name;").fetchall()

        if len(query_result):
            self.film_table_data.setRowCount(len(query_result))
            self.film_table_data.setColumnCount(len(query_result[0]))
            titles = ["ИД", "Название фильма", "Жанр", "Продолжительность", "Начало", "Кинотеатр", "Зал", "Цена"]
            self.film_table_data.setHorizontalHeaderLabels(titles)

            for i, elem in enumerate(query_result):
                for j, val in enumerate(elem):
                    self.film_table_data.setItem(i, j, QTableWidgetItem(str(val)))
            self.film_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            self.clear_table()

    def clear_table(self):
        while self.film_table_data.rowCount() > 0:
            self.film_table_data.removeRow(0)

    def add_film(self):
        create_film.setWindowTitle("Добавление фильма")
        create_film.show()

    def delete_film(self):
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный фильм?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            film_id = int(self.film_table_data.item(row, 0).text())
            cursor.execute(f"DELETE FROM films WHERE id={film_id}")
            cursor.execute(f"DELETE FROM seats WHERE film={film_id}")
            connection.commit()
            self.load_film_data()


class AllGenres(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("genres.ui", self)
        self.setFixedWidth(710)
        self.initUI()

    def initUI(self):
        self.add_genre_button.clicked.connect(self.add_genre)
        self.edit_genre_button.clicked.connect(self.change_genre)
        self.delete_genre_button.clicked.connect(self.delete_genre)
        self.load_genre_data()

    def load_genre_data(self):
        query_result = cursor.execute(f"SELECT * FROM GENRES").fetchall()

        if len(query_result):
            self.genre_table_data.setRowCount(len(query_result))
            self.genre_table_data.setColumnCount(len(query_result[0]))
            titles = ["ИД", "Название жанра"]
            self.genre_table_data.setHorizontalHeaderLabels(titles)

            for i, elem in enumerate(query_result):
                for j, val in enumerate(elem):
                    self.genre_table_data.setItem(i, j, QTableWidgetItem(str(val)))
            self.genre_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            self.clear_table()

    def clear_table(self):
        while self.genre_table_data.rowCount() > 0:
            self.genre_table_data.removeRow(0)

    def add_genre(self):
        create_genre.setWindowTitle("Добавление жанра")
        create_genre.show()

    def change_genre(self):
        row = self.genre_table_data.currentRow()

        if row >= 0:
            title = self.genre_table_data.item(row, 1).text()
            create_genre.fill_data(title)
            create_genre.editing = True
            create_genre.id = int(self.genre_table_data.item(row, 0).text())
            create_genre.setWindowTitle("Изменение жанра")
            create_genre.show()

    def delete_genre(self):
        row = self.genre_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный жанр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            genre_id = int(self.genre_table_data.item(row, 0).text())
            cursor.execute(f"DELETE FROM films WHERE genre={genre_id}")
            cursor.execute(f"DELETE FROM genres WHERE id={genre_id}")
            connection.commit()
            self.load_genre_data()
            all_films.load_film_data()


class AllCinemas(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("cinemas.ui", self)
        self.setFixedWidth(711)
        self.initUI()

    def initUI(self):
        self.add_cinema_button.clicked.connect(self.add_cinema)
        self.delete_cinema_button.clicked.connect(self.delete_cinema)
        self.load_cinema_data()

    def load_cinema_data(self):
        query_result = cursor.execute(f"SELECT * FROM cinemas").fetchall()

        if len(query_result):
            self.cinema_table_data.setRowCount(len(query_result))
            self.cinema_table_data.setColumnCount(len(query_result[0]))
            titles = ["ID", "Имя"]
            self.cinema_table_data.setHorizontalHeaderLabels(titles)

            for i, elem in enumerate(query_result):
                for j, val in enumerate(elem):
                    self.cinema_table_data.setItem(i, j, QTableWidgetItem(str(val)))
            self.cinema_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            self.clear_table()

    def add_cinema(self):
        create_cinema.show()

    def clear_table(self):
        while self.cinema_table_data.rowCount() > 0:
            self.cinema_table_data.removeRow(0)

    def delete_cinema(self):
        row = self.cinema_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный кинотеатр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cinema_id = int(self.cinema_table_data.item(row, 0).text())
            cursor.execute(f"DELETE FROM films WHERE cinema={cinema_id}")
            cursor.execute(f"DELETE FROM rooms WHERE cinema={cinema_id}")
            cursor.execute(f"DELETE FROM cinemas WHERE id={cinema_id}")
            connection.commit()
            self.load_cinema_data()
            all_films.load_film_data()
            all_rooms.load_rooms_data()


class AllRooms(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("rooms.ui", self)
        self.setFixedWidth(711)
        self.initUI()

    def initUI(self):
        self.add_room_button.clicked.connect(self.add_room)
        self.delete_room_button.clicked.connect(self.delete_room)
        self.load_rooms_data()

    def load_rooms_data(self):
        query_result = cursor.execute(f"SELECT * FROM rooms").fetchall()

        if len(query_result):
            self.room_table_data.setRowCount(len(query_result))
            self.room_table_data.setColumnCount(len(query_result[0]))
            titles = ["ID", "ID кинотеатра", "Число рядов", "Число мест в ряду"]
            self.room_table_data.setHorizontalHeaderLabels(titles)

            for i, elem in enumerate(query_result):
                for j, val in enumerate(elem):
                    self.room_table_data.setItem(i, j, QTableWidgetItem(str(val)))
            self.room_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        else:
            self.clear_table()

    def clear_table(self):
        while self.room_table_data.rowCount() > 0:
            self.room_table_data.removeRow(0)

    def add_room(self):
        create_room.show()

    def delete_room(self):
        row = self.room_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный зал?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            room_id = int(self.room_table_data.item(row, 0).text())
            cursor.execute(f"DELETE FROM films WHERE room={room_id}")
            cursor.execute(f"DELETE FROM seats WHERE room={room_id}")
            cursor.execute(f"DELETE FROM rooms WHERE id={room_id}")
            connection.commit()
            self.load_rooms_data()
            all_films.load_film_data()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    create_afisha = CreateAfisha()
    create_film = CreateFilm()
    create_genre = CreateGenre()
    create_cinema = CreateCinema()
    create_room = CreateRoom()
    all_cinemas = AllCinemas()
    all_films = AllFilms()
    all_genres = AllGenres()
    all_rooms = AllRooms()
    main_admin_window = AdminMainWindow()
    login_window = LoginWindow()
    register_window = RegisterWindow()
    login_window.show()
    sys.exit(app.exec_())
