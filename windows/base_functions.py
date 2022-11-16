from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView
import sqlite3
import datetime as dt


connection = sqlite3.connect("data/CinemaSystemDatabase.db")
cursor = connection.cursor()


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def create_table(titles: list, query_result: list, table: QTableWidget, equal_cols: bool = True,
                 need_datetime=False, column=-1) -> None:
    """
    fills table with taken column titles,
    using data from query_result
    """
    table.setRowCount(len(query_result))
    table.setColumnCount(len(query_result[0]))
    table.setHorizontalHeaderLabels(titles)

    for i, elem in enumerate(query_result):
        for j, val in enumerate(elem):
            table.setItem(i, j, QTableWidgetItem(str(val)))

    table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # set table read only
    if equal_cols:
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # to set columns equal width
    if need_datetime:
        format_datetime(table, column)


def format_datetime(table: QTableWidget, column: int):
    """
    format datetime in tables
    """
    for row in range(table.rowCount()):
        datetime = table.item(row, column).text()
        formated_datetime = dt.datetime(*map(int, datetime.split())).strftime("%d.%m.%Y %H:%M")
        table.item(row, column).setText(formated_datetime)


def delete_seanses():
    all_seances = cursor.execute("SELECT id, datetime FROM films").fetchall()
    to_update = list()
    for seanse in all_seances:
        if check_date(seanse[1]):
            to_update.append(str(seanse[0]))
    if to_update:
        cursor.execute(f"UPDATE films set can_buy=0 WHERE id IN ({', '.join(to_update)})")
        connection.commit()


def check_date(datetime_str: str):
    date_and_time = dt.datetime(*map(int, datetime_str.split()))
    if date_and_time <= dt.datetime.now():
        return True
    return False
