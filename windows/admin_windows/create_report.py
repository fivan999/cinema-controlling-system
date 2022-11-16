from PyQt5.QtWidgets import QWidget, QMessageBox
from data.py_files.ui_code import Ui_CreateReport
from windows.base_functions import connection, cursor
from collections import defaultdict
import datetime as dt
import os
import csv
import matplotlib.pyplot as plt


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
