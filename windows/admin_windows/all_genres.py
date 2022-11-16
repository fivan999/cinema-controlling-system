from PyQt5.QtWidgets import QWidget, QInputDialog, QMessageBox
from data.py_files.ui_code import Ui_AllGenres
from windows.base_functions import connection, cursor, create_table


class AllGenres(QWidget, Ui_AllGenres):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(710)
        self.initUI()

    def initUI(self) -> None:
        self.update_button.clicked.connect(self.load_genre_data)
        self.add_genre_button.clicked.connect(self.add_genre)
        self.edit_genre_button.clicked.connect(self.change_genre)
        self.delete_genre_button.clicked.connect(self.delete_genre)
        self.load_genre_data()

    def load_genre_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM GENRES").fetchall()

        if query_result:
            titles = ["ИД", "Название жанра"]
            create_table(titles, query_result, self.genre_table_data)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.genre_table_data.rowCount() > 0:
            self.genre_table_data.removeRow(0)

    def add_genre(self) -> None:
        name, ok_pressed = QInputDialog.getText(self, "Жанр",
                                                "Введите имя нового жанра")
        if ok_pressed:
            if name:
                cursor.execute(f"INSERT INTO genres(name) "
                               f"VALUES (?)", (name,))
                connection.commit()
                self.load_genre_data()
            else:
                QMessageBox.critical(self, "Ошибка",
                                     "Неверно заполнена форма")

    def change_genre(self) -> None:
        row = self.genre_table_data.currentRow()

        if row >= 0:
            name, ok_pressed = QInputDialog.getText(self, "Жанр",
                                                    "Введите имя нового жанра")
            if ok_pressed:
                if name:
                    cursor.execute(f"UPDATE genres SET name=? "
                                   f"WHERE id=?", (name, int(self.genre_table_data.item(row, 0).text())))
                    connection.commit()
                    self.load_genre_data()
                else:
                    QMessageBox.critical(self, "Ошибка",
                                         "Неверно заполнена форма")

    def delete_genre(self) -> None:
        row = self.genre_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, 'Удаление жанра', "Действительно удалить данный жанр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            genre_id = int(self.genre_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE genre={genre_id}; "
                                 f"DELETE FROM genres WHERE id={genre_id}")
            connection.commit()
            self.load_genre_data()
