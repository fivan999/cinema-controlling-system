from PyQt5.QtWidgets import QWidget
from data.py_files.ui_code import Ui_CreateRoom
from windows.base_functions import connection, cursor


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
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()
