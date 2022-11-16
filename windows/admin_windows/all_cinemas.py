from PyQt5.QtWidgets import QWidget, QInputDialog, QMessageBox
from data.py_files.ui_code import Ui_AllCinemas
from windows.admin_windows.create_report import CreateReport
from windows.base_functions import connection, cursor, create_table


class AllCinemas(QWidget, Ui_AllCinemas):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.report = CreateReport()
        self.setFixedWidth(711)
        self.initUI()

    def initUI(self) -> None:
        self.update_button.clicked.connect(self.load_cinema_data)
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
