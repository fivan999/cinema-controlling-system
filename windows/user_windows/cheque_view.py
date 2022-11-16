from PyQt5.QtWidgets import QWidget, QMessageBox
from data.py_files.ui_code import Ui_ChequeView
import os


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
