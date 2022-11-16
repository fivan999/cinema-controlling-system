from PyQt5.QtWidgets import QWidget
from data.py_files.ui_code import Ui_UserProfile
from windows.user_windows.cheque_view import ChequeView
from windows.base_functions import cursor, create_table


class UserProfile(QWidget, Ui_UserProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.update_button.clicked.connect(lambda: self.fill(self.user_id))

    def fill(self, user_id: int) -> None:
        self.user_id = user_id
        self.cheque_view = ChequeView()
        user_data = cursor.execute(f"SELECT username, total FROM users WHERE id={user_id}").fetchone()
        self.user_id_edit.setText(str(user_id))
        self.username_edit.setText(user_data[0])
        self.total_money_edit.setText(str(user_data[1]))
        self.watch_cheque_button.clicked.connect(self.watch_cheque)
        self.load_cheques_data(user_id)

    def load_cheques_data(self, user_id):
        query_result = cursor.execute(f"SELECT "
                                      f"cheques.id, cheques.key, films.name, films.datetime "
                                      f"FROM cheques "
                                      f"INNER JOIN films ON films.id = cheques.film "
                                      f"WHERE cheques.user = {user_id}"
                                      ).fetchall()

        if query_result:
            titles = ["ID", "Ключ", "Название фильма", "Начало фильма"]
            create_table(titles, query_result, self.purchase_table_data, need_datetime=True, column=3)

    def watch_cheque(self):
        row = self.purchase_table_data.currentRow()
        if row == -1:
            return

        filename = 'data/cheques/cheque_' + self.purchase_table_data.item(row, 0).text()
        self.cheque_view.fill(filename)
