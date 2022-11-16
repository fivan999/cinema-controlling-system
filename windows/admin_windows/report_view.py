from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from data.py_files.ui_code import Ui_ReportView
from windows.base_functions import create_table
import csv


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
