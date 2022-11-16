from PyQt5.QtWidgets import QMainWindow, QMenu, QMenuBar, QAction, QMessageBox
from windows.base_functions import delete_seanses, connection, cursor
from data.py_files.ui_code import Ui_AdminMainWindow, Ui_UserMainWindow, \
    Ui_Register, Ui_Login

from windows.admin_windows.all_cinemas import AllCinemas
from windows.admin_windows.all_rooms import AllRooms
from windows.admin_windows.all_films import AllFilms
from windows.admin_windows.all_genres import AllGenres
from windows.admin_windows.all_users import AllUsers
from windows.admin_windows.all_reports import AllReports
from windows.user_windows.user_films import UserFilms
from windows.user_windows.user_profile import UserProfile
import hashlib


class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_menubar()
        self.login_window = LoginWindow()
        self.login_window.show()
        delete_seanses()

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


class RegisterWindow(QMainWindow, Ui_Register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.setFixedSize(307, 213)
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self) -> None:
        self.clear_edits()
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

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
        self.clear_edits()

    def clear_edits(self) -> None:
        self.login_edit.clear()
        self.password_edit.clear()
        self.password_again.clear()


class LoginWindow(QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.register_window = RegisterWindow()
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
                self.cur_window = AdminMainWindow()
            else:
                self.cur_window = UserMainWindow()
                self.cur_window.user_profile.fill(user_id)
                self.cur_window.user_films.user_id = user_id
            self.clear_edits()
            self.cur_window.show()
        else:
            QMessageBox.critical(
                self, 'Ошибка входа', "Неправильный логин или пароль",
                QMessageBox.Ok)
            return

    def register(self) -> None:
        self.clear_edits()
        self.register_window.show()

    def clear_edits(self) -> None:
        self.login_edit.clear()
        self.password_edit.clear()
