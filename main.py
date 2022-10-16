import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QMessageBox, QTableWidgetItem, QHeaderView
import sqlite3


connection = sqlite3.connect("CinemaSystemDatabase.db")
cursor = connection.cursor()


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
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин")
            return
        if not password_text:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль")
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
                self, 'Ошибка входа', "Неравильный логин или пароль")
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
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин")
            return
        if not password_text or not password_text_again:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль и подтвердите его")
            return
        if password_text != password_text_again:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Пароли не совпадают")
            return

        user_obj = cursor.execute(f"SELECT username FROM users WHERE username = '{login_text}'").fetchall()
        if user_obj:
            QMessageBox.question(
                self, 'Ошибка ввода пароля', "Такой пользователь уже существует")
            return

        cursor.execute(f"INSERT INTO USERS(username, password, admin) "
                       f"VALUES('{login_text}', '{password_text}', 0)")
        QMessageBox.question(
            self, 'Успех', "Успешно создание пользователя!")
        connection.commit()
        self.clear()

    def clear(self):
        self.login_edit.clear()
        self.password_edit.clear()
        self.password_again.clear()


class MainAdminWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("admin_main_window.ui", self)
        self.setFixedWidth(710)
        self.setWindowTitle("Фильмотека")
        self.tabWidget.addTab(all_films, "Фильмы")
        self.tabWidget.addTab(all_genres, "Жанры")


class CreateFilm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("create_film.ui", self)
        self.setFixedWidth(261)
        self.id = None
        self.save_button.clicked.connect(self.define_action)
        genres = cursor.execute("SELECT name FROM genres").fetchall()
        self.genre_combo_box.addItems([item[0] for item in genres])
        self.start_time_edit.setDisplayFormat("dd/MM/yyyy hh:mm")
        self.editing = False

    def define_action(self):
        if self.editing:
            self.update_film()
            self.editing = False
        else:
            self.create_film()

    def fill_data(self, row):
        pass

    def clear_form(self):
        self.title_edit.clear()
        self.year_spin_box.clear()
        self.length_spin_box.clear()

    def update_film(self):
        self.feedback_label.setText("")
        name = self.name_edit.text()
        genre = self.genre_combo_box.currentText()
        duration = self.duration_box.value()
        start_time = self.start_time_edit.value()
        room_id = self.room_box.value()
        cinema_id = self.cinema_box.value()

        if name and duration and room_id and cinema_id:
            genre = cursor.execute(f"SELECT id FROM genres WHERE name='{genre}'").fetchone()[0]
            # cursor.execute(f"UPDATE films SET name = '{name}', year = {year}, "
            #                f"genre = {genre}, duration = {duration} "
            #                f"WHERE id = {self.id} ")
            connection.commit()
            all_films.load_film_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def create_film(self):
        try:
            self.feedback_label.setText("")
            name = self.name_edit.text()
            genre = self.genre_combo_box.currentText()
            duration = self.duration_box.value()
            start_time = self.start_time_edit.dateTime().toString(self.start_time_edit.displayFormat())
            room_id = self.room_id_box.value()
            cinema_id = self.cinema_id_box.value()
            print(start_time)

            if name and duration:
                genre = cursor.execute(f"SELECT id FROM genres WHERE name='{genre}'").fetchone()[0]
                # cursor.execute(f"INSERT INTO films(title, year, genre, duration) "
                #                f"VALUES ('{title}', {year}, {genre}, {duration}) ")
                connection.commit()
                all_films.load_film_data()
                self.close()
            else:
                self.feedback_label.setText("Неверно заполнена форма")
        except Exception as e:
            print(e)

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
            cursor.execute(f"UPDATE genres SET title = '{title}' "           
                           f"WHERE id={self.id}")
            connection.commit()
            all_genres.load_genre_data()
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


class AllFilms(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("films.ui", self)
        self.setFixedWidth(710)
        self.initUI()

    def initUI(self):
        self.add_film_button.clicked.connect(self.add_film)
        self.change_film_button.clicked.connect(self.change_film)
        self.delete_film_button.clicked.connect(self.delete_film)
        self.load_film_data()

    def load_film_data(self):
        query_result = cursor.execute(f"SELECT "
                                      f"films.id, films.name, genres.name, films.duration, "
                                      f"films.datetime, cinemas.name, rooms.id "
                                      f"FROM films "
                                      f"INNER JOIN genres ON genres.id = films.genre "
                                      f"INNER JOIN cinemas ON cinemas.id = films.cinema "
                                      f"INNER JOIN rooms ON rooms.id = films.room "
                                      f"ORDER BY films.name;").fetchall()

        if len(query_result):
            self.film_table_data.setRowCount(len(query_result))
            self.film_table_data.setColumnCount(len(query_result[0]))
            titles = ["ИД", "Название фильма", "Жанр", "Продолжительность", "Начало", "Кинотеатр", "Зал"]
            self.film_table_data.setHorizontalHeaderLabels(titles)

            for i, elem in enumerate(query_result):
                for j, val in enumerate(elem):
                    self.film_table_data.setItem(i, j, QTableWidgetItem(str(val)))
            self.film_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def add_film(self):
        create_film.setWindowTitle("Добавление фильма")
        create_film.show()

    def change_film(self):
        row = self.film_table_data.currentRow()

        if row >= 0:
            row_data = list()
            for i in range(5):
                row_data.append(self.film_table_data.item(row, i).text())
            create_film.fill_data(row_data)
            create_film.editing = True
            create_film.setWindowTitle("Изменение фильма")
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
            cursor.execute(f"DELETE FROM films WHERE genre = {genre_id}")
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
        # query_result = cursor.execute(f"SELECT * FROM GENRES").fetchall()
        #
        # if len(query_result):
        #     self.genre_table_data.setRowCount(len(query_result))
        #     self.genre_table_data.setColumnCount(len(query_result[0]))
        #     titles = ["ИД", "Название жанра"]
        #     self.genre_table_data.setHorizontalHeaderLabels(titles)
        #
        #     for i, elem in enumerate(query_result):
        #         for j, val in enumerate(elem):
        #             self.genre_table_data.setItem(i, j, QTableWidgetItem(str(val)))
        #     self.genre_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)\
        pass

    def add_cinema(self):
        create_cinema.show()

    def delete_cinema(self):
        # row = self.genre_table_data.currentRow()
        # if row == -1:
        #     return
        #
        # valid = QMessageBox.question(
        #         self, '', "Действительно удалить данный жанр?",
        #         QMessageBox.Yes, QMessageBox.No)
        #
        # if valid == QMessageBox.Yes:
        #     genre_id = int(self.genre_table_data.item(row, 0).text())
        #     cursor.execute(f"DELETE FROM films WHERE genre = {genre_id}")
        #     cursor.execute(f"DELETE FROM genres WHERE id={genre_id}")
        #     connection.commit()
        #     self.load_genre_data()
        #     all_films.load_film_data()
        pass


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
            titles = ["ID", "Номер"]
            self.room_table_data.setHorizontalHeaderLabels(titles)

            for i, elem in enumerate(query_result):
                for j, val in enumerate(elem):
                    self.genre_table_data.setItem(i, j, QTableWidgetItem(str(val)))
            self.genre_table_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        pass

    def add_room(self):
        # create_genre.setWindowTitle("Добавление жанра")
        # create_genre.show()
        pass

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
            self.load_room_data()
            all_films.load_film_data()
            self.load_rooms_data()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    create_film = CreateFilm()
    create_genre = CreateGenre()
    create_cinema = CreateCinema()
    all_cinemas = AllCinemas()
    all_films = AllFilms()
    all_genres = AllGenres()
    all_rooms = AllRooms()
    main_admin_window = MainAdminWindow()
    login_window = LoginWindow()
    register_window = RegisterWindow()
    login_window.show()
    sys.exit(app.exec_())
