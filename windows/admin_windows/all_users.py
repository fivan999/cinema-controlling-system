from PyQt5.QtWidgets import QWidget
from data.py_files.ui_code import Ui_AllUsers
from windows.base_functions import cursor, create_table


class AllUsers(QWidget, Ui_AllUsers):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_users_data()

    def load_users_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM users").fetchall()
        titles = ["ID", "Имя", "Пароль", "Админ", "Сумма покупок"]
        create_table(titles, query_result, self.users_table_data)