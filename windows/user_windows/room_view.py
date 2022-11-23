from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from data.py_files.ui_code import Ui_RoomView
from windows.base_functions import connection, cursor
import datetime as dt
from random import choice


class RoomView(QWidget, Ui_RoomView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buy_button.clicked.connect(self.buy_seat)
        self.film_id, self.price = 0, 0
        self.cur_row, self.cur_col = -1, -1
        self.user_id = 0
        self.first_seat_id = 0
        self.rows, self.cols = 0, 0

    def fill(self, film_id: int, price: int, user_id: int) -> None:
        self.user_id = user_id
        self.film_id, self.price = film_id, price
        query_result = cursor.execute("SELECT seats.id, seats.taken, rooms.id, rooms.rows, rooms.cols "
                                      "FROM seats "
                                      "INNER JOIN rooms ON rooms.id = seats.room "
                                      f"WHERE seats.film = {self.film_id}").fetchall()
        self.setWindowTitle(f"Зал {query_result[0][2]}")
        self.first_seat_id = query_result[0][0]
        self.rows, self.cols = query_result[0][3:]

        for row_ind in range(self.rows):
            for col_ind in range(self.cols):
                button = QPushButton(self)
                if not query_result[row_ind * self.cols + col_ind][1]:
                    button.setStyleSheet("background-color: green")
                    button.setText(f"{row_ind + 1}   {self.cols - col_ind}")
                    button.clicked.connect(self.take_seat)
                else:
                    button.setStyleSheet("background-color: red")
                self.seats_grid.addWidget(button, row_ind, col_ind)

    def take_seat(self) -> None:
        self.cur_row, self.cur_col = map(int, self.sender().text().split())
        self.row_edit.setText(str(self.cur_row))
        self.col_edit.setText(str(self.cur_col))

    def buy_seat(self) -> None:
        if self.cur_row >= 0 and self.cur_col >= 0:
            valid = QMessageBox.question(self, "Билет",
                                         "Действительно купить этот билет?",
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                cursor.execute(f"UPDATE users SET total=total+{self.price} WHERE "
                               f"id={self.user_id}")
                cursor.execute("UPDATE seats SET taken=1 WHERE "
                               f"id={self.first_seat_id + (self.cur_row - 1) * self.cols + (self.cols - self.cur_col)}")
                unique_cheque_key = self.generate_random_key()
                cheque_id = cursor.execute("INSERT INTO cheques(key, user, film) "
                                           f"VALUES('{unique_cheque_key}', {self.user_id}, "
                                           f"{self.film_id}) RETURNING id").fetchone()[0]
                connection.commit()
                self.create_text_cheque(cheque_id,
                                        dt.datetime.now().strftime("%d.%m.%Y %H:%M"),
                                        unique_cheque_key)
                self.close()

    def create_text_cheque(self, cheque_id: int, datetime: str, unique_cheque_key: str) -> None:
        """
        creates cheques to user's purchase
        """
        cheque_path = f"data/cheques/cheque_{cheque_id}"

        film_data = cursor.execute("SELECT films.name, cinemas.name, films.room, films.datetime, films.price "
                                   "FROM films "
                                   "INNER JOIN cinemas ON films.cinema=cinemas.id "
                                   f"WHERE films.id={self.film_id}").fetchone()

        with open(cheque_path, "w", encoding="utf-8") as cheque:
            cheque.write("Чек\n---------------------------------------\n"
                         f"Название фильма: {film_data[0]}\n"
                         f"Название кинотеатра: {film_data[1]}\n"
                         f"ID зала: {film_data[2]}\n"
                         f"Начало фильма: {dt.datetime(*map(int, film_data[3].split())).strftime('%d.%m.%Y %H:%M')}\n"
                         f"Номер чека: {cheque_id}\n"
                         f"Уникальный ключ: {unique_cheque_key}\n"
                         f"Время покупки: {datetime}\n"
                         f"Ряд: {self.cur_row}, место: {self.cur_col}\n"
                         f"Сумма покупки: {film_data[4]}\n"
                         f"---------------------------------------\n"
                         f"Спасибо за покупку!")

            QMessageBox.warning(self, "Чек",
                                f"Чек сохранен в файле: {cheque_path}",
                                QMessageBox.Ok)

    @staticmethod
    def generate_random_key() -> str:
        chars = "+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        result = ''.join([choice(chars) for _ in range(10)])
        return result

    def clear_form(self) -> None:
        self.row_edit.setText("")
        self.col_edit.setText("")
        self.cur_row, self.cur_col = -1, -1
        while self.seats_grid.count():
            child = self.seats_grid.takeAt(0)
            childWidget = child.widget()
            if childWidget:
                childWidget.setParent(None)
                childWidget.deleteLater()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.clear_form()
