from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdminMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(710, 481)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 711, 481))
        self.tabWidget.setObjectName("tabWidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class Ui_AllCinemas(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 457)
        self.add_cinema_button = QtWidgets.QPushButton(Form)
        self.add_cinema_button.setGeometry(QtCore.QRect(10, 10, 121, 23))
        self.add_cinema_button.setObjectName("add_cinema_button")
        self.cinema_table_data = QtWidgets.QTableWidget(Form)
        self.cinema_table_data.setGeometry(QtCore.QRect(10, 40, 691, 411))
        self.cinema_table_data.setObjectName("cinema_table_data")
        self.cinema_table_data.setColumnCount(0)
        self.cinema_table_data.setRowCount(0)
        self.delete_cinema_button = QtWidgets.QPushButton(Form)
        self.delete_cinema_button.setGeometry(QtCore.QRect(140, 10, 121, 23))
        self.delete_cinema_button.setObjectName("delete_cinema_button")
        self.report_button = QtWidgets.QPushButton(Form)
        self.report_button.setGeometry(QtCore.QRect(270, 10, 121, 23))
        self.report_button.setObjectName("report_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_cinema_button.setText(_translate("Form", "Добавить кинотеатр"))
        self.delete_cinema_button.setText(_translate("Form", "Удалить кинотеатр"))
        self.report_button.setText(_translate("Form", "Создать отчет"))


class Ui_CreateAfisha(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(236, 211)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 16))
        self.label.setObjectName("label")
        self.description_edit = QtWidgets.QPlainTextEdit(Form)
        self.description_edit.setGeometry(QtCore.QRect(10, 30, 221, 111))
        self.description_edit.setObjectName("description_edit")
        self.load_img_button = QtWidgets.QPushButton(Form)
        self.load_img_button.setGeometry(QtCore.QRect(10, 150, 221, 23))
        self.load_img_button.setObjectName("load_img_button")
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(160, 180, 71, 23))
        self.save_button.setObjectName("save_button")
        self.feedback_label = QtWidgets.QLabel(Form)
        self.feedback_label.setGeometry(QtCore.QRect(10, 180, 151, 21))
        self.feedback_label.setText("")
        self.feedback_label.setObjectName("feedback_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Введите описание фильма:"))
        self.load_img_button.setText(_translate("Form", "Загрузить картинку"))
        self.save_button.setText(_translate("Form", "Сохранить"))


class Ui_CreateFilm(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(261, 312)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 71, 16))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.name_edit = QtWidgets.QLineEdit(Form)
        self.name_edit.setGeometry(QtCore.QRect(90, 10, 161, 20))
        self.name_edit.setObjectName("name_edit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 51, 21))
        self.label_3.setObjectName("label_3")
        self.genre_combo_box = QtWidgets.QComboBox(Form)
        self.genre_combo_box.setGeometry(QtCore.QRect(90, 50, 161, 22))
        self.genre_combo_box.setObjectName("genre_combo_box")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 81, 21))
        self.label_4.setObjectName("label_4")
        self.duration_box = QtWidgets.QSpinBox(Form)
        self.duration_box.setGeometry(QtCore.QRect(90, 90, 161, 22))
        self.duration_box.setMaximum(999999)
        self.duration_box.setObjectName("duration_box")
        self.start_time_edit = QtWidgets.QDateTimeEdit(Form)
        self.start_time_edit.setGeometry(QtCore.QRect(90, 130, 161, 22))
        self.start_time_edit.setObjectName("start_time_edit")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 81, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 170, 81, 21))
        self.label_6.setObjectName("label_6")
        self.room_id_box = QtWidgets.QSpinBox(Form)
        self.room_id_box.setGeometry(QtCore.QRect(90, 170, 161, 22))
        self.room_id_box.setMaximum(99999)
        self.room_id_box.setObjectName("room_id_box")
        self.cinema_id_box = QtWidgets.QSpinBox(Form)
        self.cinema_id_box.setGeometry(QtCore.QRect(90, 210, 161, 22))
        self.cinema_id_box.setMaximum(9999)
        self.cinema_id_box.setObjectName("cinema_id_box")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 210, 81, 21))
        self.label_7.setObjectName("label_7")
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(180, 280, 71, 23))
        self.save_button.setObjectName("save_button")
        self.feedback_label = QtWidgets.QLabel(Form)
        self.feedback_label.setGeometry(QtCore.QRect(10, 280, 161, 20))
        self.feedback_label.setText("")
        self.feedback_label.setObjectName("feedback_label")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(10, 250, 81, 21))
        self.label_8.setObjectName("label_8")
        self.price_box = QtWidgets.QSpinBox(Form)
        self.price_box.setGeometry(QtCore.QRect(90, 250, 161, 22))
        self.price_box.setMaximum(99999999)
        self.price_box.setObjectName("price_box")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название:"))
        self.label_3.setText(_translate("Form", "Жанр:"))
        self.label_4.setText(_translate("Form", "Длительность:"))
        self.label_5.setText(_translate("Form", "Начало:"))
        self.label_6.setText(_translate("Form", "ID зала:"))
        self.label_7.setText(_translate("Form", "ID кинотеатра:"))
        self.save_button.setText(_translate("Form", "Сохранить"))
        self.label_8.setText(_translate("Form", "Цена:"))


class Ui_CreateGenreOrCinema(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(259, 76)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName("label")
        self.name_edit = QtWidgets.QLineEdit(Form)
        self.name_edit.setGeometry(QtCore.QRect(70, 10, 181, 20))
        self.name_edit.setObjectName("name_edit")
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(160, 40, 91, 23))
        self.save_button.setObjectName("save_button")
        self.feedback_label = QtWidgets.QLabel(Form)
        self.feedback_label.setGeometry(QtCore.QRect(10, 40, 141, 21))
        self.feedback_label.setText("")
        self.feedback_label.setObjectName("feedback_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название:"))
        self.save_button.setText(_translate("Form", "Сохранить"))


class Ui_CreateReport(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(241, 130)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 211, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 221, 31))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.cinema_labels = QtWidgets.QLineEdit(Form)
        self.cinema_labels.setGeometry(QtCore.QRect(10, 70, 221, 20))
        self.cinema_labels.setObjectName("cinema_labels")
        self.save_report_button = QtWidgets.QPushButton(Form)
        self.save_report_button.setGeometry(QtCore.QRect(160, 100, 71, 23))
        self.save_report_button.setObjectName("save_report_button")
        self.feedback_label = QtWidgets.QLabel(Form)
        self.feedback_label.setGeometry(QtCore.QRect(10, 100, 141, 21))
        self.feedback_label.setText("")
        self.feedback_label.setObjectName("feedback_label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Введите id кинотеатров через пробел"))
        self.label_2.setText(_translate("Form", "Введите \'все\', если хотите сделать отчет по всем кинотеатрам"))
        self.save_report_button.setText(_translate("Form", "Создать"))


class Ui_CreateRoom(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(345, 131)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 21))
        self.label.setObjectName("label")
        self.rows_box = QtWidgets.QSpinBox(Form)
        self.rows_box.setGeometry(QtCore.QRect(150, 10, 181, 22))
        self.rows_box.setMaximum(99999)
        self.rows_box.setObjectName("rows_box")
        self.feedback_label = QtWidgets.QLabel(Form)
        self.feedback_label.setGeometry(QtCore.QRect(10, 100, 211, 20))
        self.feedback_label.setText("")
        self.feedback_label.setObjectName("feedback_label")
        self.save_button = QtWidgets.QPushButton(Form)
        self.save_button.setGeometry(QtCore.QRect(250, 100, 81, 21))
        self.save_button.setObjectName("save_button")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 91, 21))
        self.label_2.setObjectName("label_2")
        self.cinema_box = QtWidgets.QSpinBox(Form)
        self.cinema_box.setGeometry(QtCore.QRect(150, 70, 181, 22))
        self.cinema_box.setMaximum(999999)
        self.cinema_box.setObjectName("cinema_box")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 131, 21))
        self.label_3.setObjectName("label_3")
        self.cols_box = QtWidgets.QSpinBox(Form)
        self.cols_box.setGeometry(QtCore.QRect(150, 40, 181, 22))
        self.cols_box.setMaximum(99999)
        self.cols_box.setObjectName("cols_box")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Количество рядов:"))
        self.save_button.setText(_translate("Form", "Сохранить"))
        self.label_2.setText(_translate("Form", "ID кинотеатра:"))
        self.label_3.setText(_translate("Form", "Количество мест в ряду:"))


class Ui_AfishaView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(480, 533)
        self.pic_label = QtWidgets.QLabel(Form)
        self.pic_label.setGeometry(QtCore.QRect(10, 10, 461, 281))
        self.pic_label.setText("")
        self.pic_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pic_label.setObjectName("pic_label")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(170, 300, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.name_label = QtWidgets.QLabel(Form)
        self.name_label.setGeometry(QtCore.QRect(0, 340, 471, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.name_label.setFont(font)
        self.name_label.setText("")
        self.name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label.setObjectName("name_label")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(140, 370, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.genre_label = QtWidgets.QLabel(Form)
        self.genre_label.setGeometry(QtCore.QRect(0, 410, 471, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.genre_label.setFont(font)
        self.genre_label.setText("")
        self.genre_label.setAlignment(QtCore.Qt.AlignCenter)
        self.genre_label.setObjectName("genre_label")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(140, 440, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 480, 461, 291))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.description_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description_label.sizePolicy().hasHeightForWidth())
        self.description_label.setSizePolicy(sizePolicy)
        self.description_label.setMinimumSize(QtCore.QSize(300, 30))
        self.description_label.setMaximumSize(QtCore.QSize(300, 1000))
        self.description_label.setText("")
        self.description_label.setTextFormat(QtCore.Qt.AutoText)
        self.description_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.description_label.setWordWrap(True)
        self.description_label.setObjectName("description_label")
        self.horizontalLayout.addWidget(self.description_label)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Название"))
        self.label_7.setText(_translate("Form", "Жанр"))
        self.label_8.setText(_translate("Form", "Описание"))


class Ui_AllFilms(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 457)
        self.add_film_button = QtWidgets.QPushButton(Form)
        self.add_film_button.setGeometry(QtCore.QRect(10, 10, 101, 23))
        self.add_film_button.setObjectName("add_film_button")
        self.delete_film_button = QtWidgets.QPushButton(Form)
        self.delete_film_button.setGeometry(QtCore.QRect(120, 10, 101, 23))
        self.delete_film_button.setObjectName("delete_film_button")
        self.film_table_data = QtWidgets.QTableWidget(Form)
        self.film_table_data.setGeometry(QtCore.QRect(10, 40, 691, 411))
        self.film_table_data.setObjectName("film_table_data")
        self.film_table_data.setColumnCount(0)
        self.film_table_data.setRowCount(0)
        self.create_afisha_button = QtWidgets.QPushButton(Form)
        self.create_afisha_button.setGeometry(QtCore.QRect(230, 10, 101, 23))
        self.create_afisha_button.setObjectName("create_afisha_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_film_button.setText(_translate("Form", "Добавить фильм"))
        self.delete_film_button.setText(_translate("Form", "Удалить фильм"))
        self.create_afisha_button.setText(_translate("Form", "Создать афишу"))


class Ui_AllGenres(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(710, 457)
        self.add_genre_button = QtWidgets.QPushButton(Form)
        self.add_genre_button.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.add_genre_button.setObjectName("add_genre_button")
        self.edit_genre_button = QtWidgets.QPushButton(Form)
        self.edit_genre_button.setGeometry(QtCore.QRect(110, 10, 91, 23))
        self.edit_genre_button.setObjectName("edit_genre_button")
        self.delete_genre_button = QtWidgets.QPushButton(Form)
        self.delete_genre_button.setGeometry(QtCore.QRect(210, 10, 91, 23))
        self.delete_genre_button.setObjectName("delete_genre_button")
        self.genre_table_data = QtWidgets.QTableWidget(Form)
        self.genre_table_data.setGeometry(QtCore.QRect(10, 40, 691, 411))
        self.genre_table_data.setObjectName("genre_table_data")
        self.genre_table_data.setColumnCount(0)
        self.genre_table_data.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_genre_button.setText(_translate("Form", "Добавить жанр"))
        self.edit_genre_button.setText(_translate("Form", "Изменить жанр"))
        self.delete_genre_button.setText(_translate("Form", "Удалить жанр"))


class Ui_Login(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(309, 175)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 60, 41, 16))
        self.label_2.setObjectName("label_2")
        self.login_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.login_edit.setGeometry(QtCore.QRect(120, 60, 113, 20))
        self.login_edit.setObjectName("login_edit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 100, 47, 13))
        self.label_3.setObjectName("label_3")
        self.password_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.password_edit.setGeometry(QtCore.QRect(120, 100, 113, 20))
        self.password_edit.setObjectName("password_edit")
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(70, 130, 71, 23))
        self.login_button.setObjectName("login_button")
        self.register_button = QtWidgets.QPushButton(self.centralwidget)
        self.register_button.setGeometry(QtCore.QRect(150, 130, 81, 23))
        self.register_button.setObjectName("register_button")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Вход"))
        self.label_2.setText(_translate("MainWindow", "Логин:"))
        self.label_3.setText(_translate("MainWindow", "Пароль:"))
        self.login_button.setText(_translate("MainWindow", "Вход"))
        self.register_button.setText(_translate("MainWindow", "Регистрация"))


class Ui_Register(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(307, 213)
        self.password_edit = QtWidgets.QLineEdit(Form)
        self.password_edit.setGeometry(QtCore.QRect(120, 100, 113, 20))
        self.password_edit.setObjectName("password_edit")
        self.login_button = QtWidgets.QPushButton(Form)
        self.login_button.setGeometry(QtCore.QRect(70, 170, 71, 23))
        self.login_button.setObjectName("login_button")
        self.register_button = QtWidgets.QPushButton(Form)
        self.register_button.setGeometry(QtCore.QRect(150, 170, 81, 23))
        self.register_button.setObjectName("register_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(60, 0, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(70, 60, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(70, 100, 47, 13))
        self.label_3.setObjectName("label_3")
        self.login_edit = QtWidgets.QLineEdit(Form)
        self.login_edit.setGeometry(QtCore.QRect(120, 60, 113, 20))
        self.login_edit.setObjectName("login_edit")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 140, 91, 20))
        self.label_4.setObjectName("label_4")
        self.password_again = QtWidgets.QLineEdit(Form)
        self.password_again.setGeometry(QtCore.QRect(120, 140, 113, 20))
        self.password_again.setObjectName("password_again")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.login_button.setText(_translate("Form", "Вход"))
        self.register_button.setText(_translate("Form", "Регистрация"))
        self.label.setText(_translate("Form", "Регистрация"))
        self.label_2.setText(_translate("Form", "Логин:"))
        self.label_3.setText(_translate("Form", "Пароль:"))
        self.label_4.setText(_translate("Form", "Пароль еще раз:"))


class Ui_RoomView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(476, 257)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 5)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 2, 1, 1)
        self.seats_grid = QtWidgets.QGridLayout()
        self.seats_grid.setObjectName("seats_grid")
        self.gridLayout_2.addLayout(self.seats_grid, 1, 0, 1, 5)
        self.buy_button = QtWidgets.QPushButton(Form)
        self.buy_button.setObjectName("buy_button")
        self.gridLayout_2.addWidget(self.buy_button, 2, 4, 1, 1)
        self.row_edit = QtWidgets.QLineEdit(Form)
        self.row_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.row_edit.setObjectName("row_edit")
        self.gridLayout_2.addWidget(self.row_edit, 2, 1, 1, 1)
        self.col_edit = QtWidgets.QLineEdit(Form)
        self.col_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.col_edit.setObjectName("col_edit")
        self.gridLayout_2.addWidget(self.col_edit, 2, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Ряд:"))
        self.label.setText(_translate("Form", "Экран"))
        self.label_3.setText(_translate("Form", "Место:"))
        self.buy_button.setText(_translate("Form", "Купить"))


class Ui_AllRooms(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 457)
        self.add_room_button = QtWidgets.QPushButton(Form)
        self.add_room_button.setGeometry(QtCore.QRect(10, 10, 111, 23))
        self.add_room_button.setObjectName("add_room_button")
        self.delete_room_button = QtWidgets.QPushButton(Form)
        self.delete_room_button.setGeometry(QtCore.QRect(130, 10, 101, 23))
        self.delete_room_button.setObjectName("delete_room_button")
        self.room_table_data = QtWidgets.QTableWidget(Form)
        self.room_table_data.setGeometry(QtCore.QRect(10, 40, 691, 411))
        self.room_table_data.setObjectName("room_table_data")
        self.room_table_data.setColumnCount(0)
        self.room_table_data.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_room_button.setText(_translate("Form", "Добавить кинозал"))
        self.delete_room_button.setText(_translate("Form", "Удалить кинозал"))


class Ui_UserFilms(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 396)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 741, 401))
        self.centralwidget.setObjectName("centralwidget")
        self.films_table_data = QtWidgets.QTableWidget(self.centralwidget)
        self.films_table_data.setGeometry(QtCore.QRect(10, 40, 721, 351))
        self.films_table_data.setObjectName("films_table_data")
        self.films_table_data.setColumnCount(0)
        self.films_table_data.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 21))
        self.label.setObjectName("label")
        self.search_by_box = QtWidgets.QComboBox(self.centralwidget)
        self.search_by_box.setGeometry(QtCore.QRect(70, 10, 141, 22))
        self.search_by_box.setObjectName("search_by_box")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(420, 10, 91, 23))
        self.search_button.setObjectName("search_button")
        self.search_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_edit.setGeometry(QtCore.QRect(220, 10, 191, 21))
        self.search_edit.setObjectName("search_edit")
        self.buy_ticket_button = QtWidgets.QPushButton(self.centralwidget)
        self.buy_ticket_button.setGeometry(QtCore.QRect(520, 10, 101, 23))
        self.buy_ticket_button.setObjectName("buy_ticket_button")
        self.afisha_button = QtWidgets.QPushButton(self.centralwidget)
        self.afisha_button.setGeometry(QtCore.QRect(630, 10, 101, 23))
        self.afisha_button.setObjectName("afisha_button")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Поиск по:"))
        self.search_button.setText(_translate("MainWindow", "Поиск"))
        self.buy_ticket_button.setText(_translate("MainWindow", "Купить билет"))
        self.afisha_button.setText(_translate("MainWindow", "Смотреть афишу"))


class Ui_UserMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 427)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 741, 421))
        self.tabWidget.setObjectName("tabWidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


class Ui_UserProfile(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(741, 400)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 101, 21))
        self.label_2.setObjectName("label_2")
        self.user_id_edit = QtWidgets.QLineEdit(Form)
        self.user_id_edit.setGeometry(QtCore.QRect(50, 10, 113, 20))
        self.user_id_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.user_id_edit.setReadOnly(True)
        self.user_id_edit.setObjectName("user_id_edit")
        self.username_edit = QtWidgets.QLineEdit(Form)
        self.username_edit.setGeometry(QtCore.QRect(270, 10, 151, 20))
        self.username_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.username_edit.setReadOnly(True)
        self.username_edit.setObjectName("username_edit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(430, 10, 81, 21))
        self.label_4.setObjectName("label_4")
        self.total_money_edit = QtWidgets.QLineEdit(Form)
        self.total_money_edit.setGeometry(QtCore.QRect(520, 10, 151, 20))
        self.total_money_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.total_money_edit.setReadOnly(True)
        self.total_money_edit.setObjectName("total_money_edit")
        self.purchase_table_data = QtWidgets.QTableWidget(Form)
        self.purchase_table_data.setGeometry(QtCore.QRect(10, 60, 721, 331))
        self.purchase_table_data.setObjectName("purchase_table_data")
        self.purchase_table_data.setColumnCount(0)
        self.purchase_table_data.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Мой ID:"))
        self.label_2.setText(_translate("Form", "Имя пользователя:"))
        self.label_3.setText(_translate("Form", "Мои покупки:"))
        self.label_4.setText(_translate("Form", "Сумма покупок:"))


class Ui_AllUsers(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 457)
        self.users_table_data = QtWidgets.QTableWidget(Form)
        self.users_table_data.setGeometry(QtCore.QRect(10, 10, 691, 441))
        self.users_table_data.setObjectName("users_table_data")
        self.users_table_data.setColumnCount(0)
        self.users_table_data.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
