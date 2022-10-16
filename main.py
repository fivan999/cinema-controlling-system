import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QMessageBox
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
        print(user_obj)
        if user_obj:
            is_admin = user_obj[0][0]
            if is_admin:
                pass
            else:
                pass
        else:
            QMessageBox.question(
                self, 'Ошибка входа', "Нерпвильный логин или пароль")
            return

    def register(self):
        register_window.show()
        self.clear()
        self.close()

    def clear(self):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    register_window = RegisterWindow()
    sys.exit(app.exec())
