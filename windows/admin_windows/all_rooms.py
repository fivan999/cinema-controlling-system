from PyQt5.QtWidgets import QWidget, QMessageBox
from data.py_files.ui_code import Ui_AllRooms
from windows.admin_windows.create_room import CreateRoom
from windows.base_functions import connection, cursor, create_table


class AllRooms(QWidget, Ui_AllRooms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_room = CreateRoom()
        self.initUI()

    def initUI(self) -> None:
        self.update_button.clicked.connect(self.load_rooms_data)
        self.add_room_button.clicked.connect(self.add_room)
        self.delete_room_button.clicked.connect(self.delete_room)
        self.load_rooms_data()

    def load_rooms_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM rooms").fetchall()

        if query_result:
            titles = ["ID", "ID кинотеатра", "Число рядов", "Число мест в ряду"]
            create_table(titles, query_result, self.room_table_data)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.room_table_data.rowCount() > 0:
            self.room_table_data.removeRow(0)

    def add_room(self) -> None:
        self.create_room.show()

    def delete_room(self) -> None:
        row = self.room_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, 'Удаление зала', "Действительно удалить данный зал?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            room_id = int(self.room_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE room={room_id}; "
                                 f"DELETE FROM seats WHERE room={room_id}; "
                                 f"DELETE FROM rooms WHERE id={room_id}")
            connection.commit()
            self.load_rooms_data()
