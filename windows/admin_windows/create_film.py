from PyQt5.QtWidgets import QWidget
from data.py_files.ui_code import Ui_CreateFilm
from windows.base_functions import connection, cursor
import datetime as dt


class CreateFilm(QWidget, Ui_CreateFilm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(261, 339)
        self.save_button.clicked.connect(self.create_film)
        self.create_genres_box()
        self.start_time_edit.setDisplayFormat("yyyy MM dd hh mm")
        self.update_genres_button.clicked.connect(self.create_genres_box)

    def create_genres_box(self) -> None:
        genres = cursor.execute("SELECT name FROM genres ORDER BY name").fetchall()
        self.genre_combo_box.clear()
        self.genre_combo_box.addItems([item[0] for item in genres])

    def clear_form(self) -> None:
        self.feedback_label.clear()
        self.name_edit.clear()
        self.duration_box.setValue(0)
        self.room_id_box.setValue(0)
        self.cinema_id_box.setValue(0)
        self.price_box.setValue(0)

    @staticmethod
    def check_film(room: int, start_time: str, film_duration: int) -> bool:
        start_time = dt.datetime(*map(int, start_time.split()))
        end_time = start_time + dt.timedelta(minutes=(25 + film_duration))
        if start_time < dt.datetime.now() + dt.timedelta(days=5):
            return False

        all_times = cursor.execute(f"SELECT datetime, duration FROM films WHERE room={room}").fetchall()
        for item in all_times:
            time, duration = item
            item_start_time = dt.datetime(*map(int, time.split()))
            item_end_time = item_start_time + dt.timedelta(minutes=(25 + duration))
            if item_start_time <= start_time < item_end_time or item_start_time < end_time <= item_end_time:
                print(item)
                return False

        return True

    @staticmethod
    def insert_seats(seats: int, film_id: int, room_id: int) -> None:
        query = "INSERT INTO seats(taken, room, film) VALUES"
        for _ in range(seats + 1):
            query += f" (0, {room_id}, {film_id}), "
        cursor.execute(query[:-2])

    def create_film(self) -> None:
        self.feedback_label.setText("")
        name = self.name_edit.text()
        genre = self.genre_combo_box.currentText()
        duration = self.duration_box.value()
        start_time = self.start_time_edit.dateTime().toString(self.start_time_edit.displayFormat())
        room_id = self.room_id_box.value()
        cinema_id = self.cinema_id_box.value()
        price = self.price_box.value()
        room_in_cinema = cursor.execute("SELECT id FROM rooms WHERE id=? and cinema=?",
                                        (room_id, cinema_id)).fetchone()

        if name and duration and room_id and cinema_id and room_in_cinema and self.check_film(room_id, start_time,
                                                                                              duration):
            genre_id = cursor.execute(f"SELECT id FROM genres WHERE name='{genre}'").fetchone()[0]
            rows_and_cols = cursor.execute(f"SELECT rows, cols FROM rooms WHERE id={room_id}").fetchone()
            rows_cnt, cols_cnt = rows_and_cols

            film_id = cursor.execute(f"INSERT INTO films (name, genre, duration, datetime, room, "
                                     f"cinema, price, can_buy) "
                                     f"VALUES(?, {genre_id}, {duration}, "
                                     f"?, {room_id}, {cinema_id}, {price}, 1) RETURNING id",
                                     (name, start_time)).fetchone()[0]
            self.insert_seats(rows_cnt * cols_cnt, film_id, room_id)

            connection.commit()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()
