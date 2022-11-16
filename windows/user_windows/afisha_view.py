from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from data.py_files.ui_code import Ui_AfishaView


class AfishaView(QWidget, Ui_AfishaView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(480)

    def fill(self, name: str, genre: str, description: str, image: str) -> None:
        self.setWindowTitle(name)
        self.img = QPixmap(image)
        self.img = self.img.scaledToWidth(461)
        self.img = self.img.scaledToHeight(281)
        self.pic_label.setPixmap(self.img)
        self.name_label.setText(name)
        self.description_label.setText(description)
        self.description_label.adjustSize()
        self.genre_label.setText(genre)
