from PyQt5.QtWidgets import QWidget, QFileDialog
from data.py_files.ui_code import Ui_CreateAfisha
from windows.base_functions import connection, cursor
import os
import shutil


class CreateAfisha(QWidget, Ui_CreateAfisha):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(236, 211)
        self.filename = None
        self.genre_id, self.film_name = None, None
        self.save_button.clicked.connect(self.create_afisha)
        self.load_img_button.clicked.connect(self.choose_img)

    def clear_form(self) -> None:
        self.description_edit.clear()
        self.filename = None

    def check_filename(self) -> str:
        new_fname = 'data/afisha_images/' + self.filename[self.filename.rfind('/') + 1:]
        if not os.path.isfile(new_fname):
            shutil.copyfile(self.filename, new_fname)
        return new_fname

    def create_afisha(self) -> None:
        description = self.description_edit.toPlainText()
        if description and self.filename:
            fname = self.check_filename()
            afisha_id = cursor.execute("INSERT INTO descriptions(image, description) "
                                       "VALUES(?, ?) RETURNING id", (fname, description)).fetchone()[0]
            cursor.execute(f"UPDATE films SET afisha={afisha_id} WHERE "
                           f"name=? and genre={self.genre_id}", (self.film_name, ))
            connection.commit()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def choose_img(self) -> None:
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png)')[0]
        self.filename = fname

    def closeEvent(self, event) -> None:
        self.clear_form()
