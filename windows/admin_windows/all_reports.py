from PyQt5.QtWidgets import QWidget, QMessageBox
from data.py_files.ui_code import Ui_AllReports
from windows.admin_windows.report_view import ReportView
from windows.base_functions import connection, cursor, create_table
import shutil
import os


class AllReports(QWidget, Ui_AllReports):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.report_view = ReportView()
        self.update_button.clicked.connect(self.load_report_data)
        self.delete_button.clicked.connect(self.delete_report)
        self.watch_button.clicked.connect(self.watch_report)
        self.load_report_data()

    def delete_report(self):
        row = self.reports_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
            self, 'Удаление отчета', "Действительно удалить данный отчет?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            report_id = self.reports_table_data.item(row, 0).text()
            report_path = self.reports_table_data.item(row, 1).text()
            cursor.execute(f"DELETE FROM reports WHERE id={report_id}")
            connection.commit()
            shutil.rmtree(report_path)
            self.load_report_data()

    def watch_report(self):
        row = self.reports_table_data.currentRow()
        if row == -1:
            return

        dir_name = self.reports_table_data.item(row, 1).text()
        if not os.path.isdir(dir_name):
            QMessageBox.critical(self, "Отчет", "Файл не найден",
                                 QMessageBox.Ok)
            return
        self.report_view.fill(dir_name)

    def load_report_data(self):
        query_result = cursor.execute("SELECT * FROM reports").fetchall()
        if query_result:
            titles = ["ID", "Путь к файлу", "Время создания"]
            create_table(titles, query_result, self.reports_table_data, equal_cols=False)
            self.reports_table_data.setColumnWidth(0, 30)
            self.reports_table_data.setColumnWidth(1, 317)
            self.reports_table_data.setColumnWidth(2, 318)
