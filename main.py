import csv
import os
import shutil
import sys
from collections import defaultdict
from random import choice
import sqlite3
import datetime as dt
import matplotlib.pyplot as plt
import hashlib
from PyQt5.QtGui import QPixmap, QCloseEvent
from PyQt5.QtWidgets import (QWidget, QMainWindow, QApplication, QMessageBox,
                             QTableWidgetItem, QHeaderView, QFileDialog,
                             QMenu, QMenuBar, QAction, QTableWidget, QPushButton, QInputDialog)
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdminMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(710, 500)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Администрирование"))


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
        Form.setWindowTitle(_translate("Form", "Создание афиши"))
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
        Form.setWindowTitle(_translate("Form", "Создание сеанса"))
        self.label.setText(_translate("Form", "Название:"))
        self.label_3.setText(_translate("Form", "Жанр:"))
        self.label_4.setText(_translate("Form", "Длительность:"))
        self.label_5.setText(_translate("Form", "Начало:"))
        self.label_6.setText(_translate("Form", "ID зала:"))
        self.label_7.setText(_translate("Form", "ID кинотеатра:"))
        self.save_button.setText(_translate("Form", "Сохранить"))
        self.label_8.setText(_translate("Form", "Цена:"))


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
        Form.setWindowTitle(_translate("Form", "Создание отчета"))
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
        Form.setWindowTitle(_translate("Form", "Создание зала"))
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
        MainWindow.setFixedSize(309, 175)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Вход"))
        self.label.setText(_translate("MainWindow", "Вход"))
        self.label_2.setText(_translate("MainWindow", "Логин:"))
        self.label_3.setText(_translate("MainWindow", "Пароль:"))
        self.login_button.setText(_translate("MainWindow", "Вход"))
        self.register_button.setText(_translate("MainWindow", "Регистрация"))


class Ui_Register(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
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
        Form.setWindowTitle(_translate("Form", "Регистрация"))
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
        MainWindow.setFixedSize(741, 440)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Пользователь"))


class Ui_UserProfile(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(741, 409)
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
        self.purchase_table_data.setGeometry(QtCore.QRect(10, 60, 721, 341))
        self.purchase_table_data.setObjectName("purchase_table_data")
        self.purchase_table_data.setColumnCount(0)
        self.purchase_table_data.setRowCount(0)
        self.watch_cheque_button = QtWidgets.QPushButton(Form)
        self.watch_cheque_button.setGeometry(QtCore.QRect(640, 40, 91, 21))
        self.watch_cheque_button.setObjectName("watch_cheque_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Мой ID:"))
        self.label_2.setText(_translate("Form", "Имя пользователя:"))
        self.label_3.setText(_translate("Form", "Мои покупки:"))
        self.label_4.setText(_translate("Form", "Сумма покупок:"))
        self.watch_cheque_button.setText(_translate("Form", "Посмотреть чек"))


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


class Ui_ReportView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(662, 866)
        self.image = QtWidgets.QLabel(Form)
        self.image.setGeometry(QtCore.QRect(10, 380, 640, 480))
        self.image.setText("")
        self.image.setObjectName("image")
        self.months_table_data = QtWidgets.QTableWidget(Form)
        self.months_table_data.setGeometry(QtCore.QRect(10, 10, 641, 361))
        self.months_table_data.setObjectName("tableWidget")
        self.months_table_data.setColumnCount(0)
        self.months_table_data.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Отчет"))


class Ui_ChequeView(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(322, 362)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(120, 10, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.label_2.setObjectName("label_2")
        self.film_name_edit = QtWidgets.QLineEdit(Form)
        self.film_name_edit.setGeometry(QtCore.QRect(130, 50, 181, 21))
        self.film_name_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.film_name_edit.setReadOnly(True)
        self.film_name_edit.setObjectName("film_name_edit")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 121, 21))
        self.label_3.setObjectName("label_3")
        self.cinema_name_edit = QtWidgets.QLineEdit(Form)
        self.cinema_name_edit.setGeometry(QtCore.QRect(130, 80, 181, 21))
        self.cinema_name_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.cinema_name_edit.setReadOnly(True)
        self.cinema_name_edit.setObjectName("cinema_name_edit")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 121, 21))
        self.label_4.setObjectName("label_4")
        self.film_start_edit = QtWidgets.QLineEdit(Form)
        self.film_start_edit.setGeometry(QtCore.QRect(130, 140, 181, 20))
        self.film_start_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.film_start_edit.setReadOnly(True)
        self.film_start_edit.setObjectName("film_start_edit")
        self.cheque_id_edit = QtWidgets.QLineEdit(Form)
        self.cheque_id_edit.setGeometry(QtCore.QRect(130, 170, 181, 20))
        self.cheque_id_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.cheque_id_edit.setReadOnly(True)
        self.cheque_id_edit.setObjectName("cheque_id_edit")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 170, 121, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 200, 121, 21))
        self.label_6.setObjectName("label_6")
        self.unique_key_edit = QtWidgets.QLineEdit(Form)
        self.unique_key_edit.setGeometry(QtCore.QRect(130, 200, 181, 20))
        self.unique_key_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.unique_key_edit.setReadOnly(True)
        self.unique_key_edit.setObjectName("unique_key_edit")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 140, 121, 21))
        self.label_7.setObjectName("label_7")
        self.room_id_edit = QtWidgets.QLineEdit(Form)
        self.room_id_edit.setGeometry(QtCore.QRect(130, 110, 181, 20))
        self.room_id_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.room_id_edit.setReadOnly(True)
        self.room_id_edit.setObjectName("room_id_edit")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(10, 260, 31, 21))
        self.label_8.setObjectName("label_8")
        self.row_edit = QtWidgets.QLineEdit(Form)
        self.row_edit.setGeometry(QtCore.QRect(40, 260, 111, 20))
        self.row_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.row_edit.setReadOnly(True)
        self.row_edit.setObjectName("row_edit")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(160, 260, 41, 21))
        self.label_9.setObjectName("label_9")
        self.col_edit = QtWidgets.QLineEdit(Form)
        self.col_edit.setGeometry(QtCore.QRect(200, 260, 111, 20))
        self.col_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.col_edit.setReadOnly(True)
        self.col_edit.setObjectName("col_edit")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(10, 230, 121, 21))
        self.label_10.setObjectName("label_10")
        self.buy_time_edit = QtWidgets.QLineEdit(Form)
        self.buy_time_edit.setGeometry(QtCore.QRect(130, 230, 181, 20))
        self.buy_time_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.buy_time_edit.setReadOnly(True)
        self.buy_time_edit.setObjectName("buy_time_edit")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(10, 290, 121, 21))
        self.label_11.setObjectName("label_11")
        self.total_edit = QtWidgets.QLineEdit(Form)
        self.total_edit.setGeometry(QtCore.QRect(130, 290, 181, 20))
        self.total_edit.setAlignment(QtCore.Qt.AlignCenter)
        self.total_edit.setReadOnly(True)
        self.total_edit.setObjectName("total_edit")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(10, 320, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Чек"))
        self.label.setText(_translate("Form", "Чек"))
        self.label_2.setText(_translate("Form", "Название фильма:"))
        self.label_3.setText(_translate("Form", "Название кинотеатра:"))
        self.label_4.setText(_translate("Form", "ID зала:"))
        self.label_5.setText(_translate("Form", "Номер чека:"))
        self.label_6.setText(_translate("Form", "Уникальный ключ:"))
        self.label_7.setText(_translate("Form", "Начало фильма:"))
        self.label_8.setText(_translate("Form", "Ряд:"))
        self.label_9.setText(_translate("Form", "Место:"))
        self.label_10.setText(_translate("Form", "Время покупки:"))
        self.label_11.setText(_translate("Form", "Сумма покупки:"))
        self.label_12.setText(_translate("Form", "Спасибо за покупку!"))


class Ui_AllReports(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(711, 457)
        self.delete_button = QtWidgets.QPushButton(Form)
        self.delete_button.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.delete_button.setObjectName("delete_button")
        self.watch_button = QtWidgets.QPushButton(Form)
        self.watch_button.setGeometry(QtCore.QRect(110, 10, 111, 23))
        self.watch_button.setObjectName("watch_button")
        self.reports_table_data = QtWidgets.QTableWidget(Form)
        self.reports_table_data.setGeometry(QtCore.QRect(10, 40, 691, 411))
        self.reports_table_data.setObjectName("reports_table_data")
        self.reports_table_data.setColumnCount(0)
        self.reports_table_data.setRowCount(0)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.delete_button.setText(_translate("Form", "Удалить отчет"))
        self.watch_button.setText(_translate("Form", "Посмотреть отчет"))


connection = sqlite3.connect("data/CinemaSystemDatabase.db")
cursor = connection.cursor()


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


def create_admin_windows() -> None:
    """
    creates nessesary windows for admin
    """
    global all_films, all_cinemas, all_genres, \
        all_rooms, main_admin_window, create_film, all_reports
    all_cinemas = AllCinemas()
    all_films = AllFilms()
    all_genres = AllGenres()
    all_rooms = AllRooms()
    create_film = CreateFilm()
    all_reports = AllReports()
    main_admin_window = AdminMainWindow()


def create_user_window() -> None:
    """
    creates nessesary windows for user
    """
    global user_main_window, afisha_view, user_films, user_profile
    afisha_view = AfishaView()
    user_profile = UserProfile()
    user_films = UserFilms()
    user_main_window = UserMainWindow()


def create_table(titles: list, query_result: list, table: QTableWidget, enable: bool = False) -> None:
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
            if enable:
                table.item(i, j).setFlags(QtCore.Qt.ItemIsEnabled)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # to set columns equal width


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def create_menubar(self) -> None:
        self.menuBar = QMenuBar(self)
        self.menu = QMenu("Меню", self)
        self.login_action = QAction("Смена пользователя", self)
        self.menuBar.addMenu(self.menu)
        self.menu.addAction(self.login_action)
        self.login_action.triggered.connect(self.change_user)
        self.setMenuBar(self.menuBar)

    def change_user(self) -> None:
        login_window.show()
        self.close()


class AdminMainWindow(MainWindow, Ui_AdminMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(710)
        self.create_tab_widget()
        self.create_menubar()

    def create_tab_widget(self) -> None:
        self.tabWidget.addTab(all_cinemas, "Кинотеатры")
        self.tabWidget.addTab(all_rooms, "Залы")
        self.tabWidget.addTab(all_films, "Фильмы")
        self.tabWidget.addTab(all_genres, "Жанры")
        self.tabWidget.addTab(AllUsers(), "Пользователи")
        self.tabWidget.addTab(all_reports, "Отчеты")


class UserMainWindow(MainWindow, Ui_UserMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_tab_widget()
        self.create_menubar()

    def create_tab_widget(self) -> None:
        self.tabWidget.addTab(user_films, "Фильмы")
        self.tabWidget.addTab(user_profile, "Мой профиль")


class LoginWindow(QWidget, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self) -> None:
        login_text = self.login_edit.text()
        password_text = self.password_edit.text()

        if not login_text:
            QMessageBox.critical(
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин",
                QMessageBox.Ok)
            return
        if not password_text:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль",
                QMessageBox.Ok)
            return

        password_text = hashlib.sha256(password_text.encode('utf-8')).hexdigest()
        user_obj = cursor.execute(f"SELECT id, admin FROM users WHERE username = ?"
                                  f" and password='{password_text}'", (login_text, )).fetchone()
        if user_obj:
            user_id, is_admin = user_obj
            self.clear()
            if is_admin:
                create_admin_windows()
                main_admin_window.show()
            else:
                create_user_window()
                user_profile.fill(user_id)
                user_main_window.show()
        else:
            QMessageBox.critical(
                self, 'Ошибка входа', "Неравильный логин или пароль",
                QMessageBox.Ok)
            return

    def register(self) -> None:
        register_window.show()
        self.clear()
        self.close()

    def clear(self) -> None:
        self.close()
        self.login_edit.clear()
        self.password_edit.clear()


class RegisterWindow(QWidget, Ui_Register):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.setFixedSize(307, 213)
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self) -> None:
        login_window.show()
        self.close()
        self.clear()

    def register(self) -> None:
        login_text = self.login_edit.text()
        password_text = self.password_edit.text()
        password_text_again = self.password_again.text()

        if not login_text:
            QMessageBox.critical(
                self, 'Ошибка ввода логина', "Пожалуйста, введите логин",
                QMessageBox.Ok)
            return
        if not password_text or not password_text_again:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Пожалуйста, введите пароль и подтвердите его",
                QMessageBox.Ok)
            return
        if password_text != password_text_again:
            QMessageBox.critical(
                self, 'Ошибка ввода пароля', "Пароли не совпадают",
                QMessageBox.Ok)
            return

        user_obj = cursor.execute(f"SELECT username FROM users WHERE username = ?",
                                  (login_text, )).fetchall()
        if user_obj:
            QMessageBox.critical(
                self, 'Ошибка регистрации', "Такой пользователь уже существует",
                QMessageBox.Ok)
            return

        password_text = hashlib.sha256(password_text.encode('utf-8')).hexdigest()
        cursor.execute(f"INSERT INTO USERS(username, password, admin) "
                       f"VALUES(?, ?, 0)",
                       (login_text, password_text))
        QMessageBox.information(
            self, 'Успех', "Успешно создание пользователя!",
            QMessageBox.Ok)
        connection.commit()
        self.clear()

    def clear(self) -> None:
        self.login_edit.clear()
        self.password_edit.clear()
        self.password_again.clear()


class CreateFilm(QWidget, Ui_CreateFilm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(261, 312)
        self.save_button.clicked.connect(self.create_film)
        self.create_genres_box()
        self.start_time_edit.setDisplayFormat("yyyy MM dd hh mm")

    def create_genres_box(self) -> None:
        genres = cursor.execute("SELECT name FROM genres ORDER BY name").fetchall()
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

        if name and duration and room_id and cinema_id and self.check_film(room_id, start_time, duration):
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
            all_films.load_film_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


class CreateRoom(QWidget, Ui_CreateRoom):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(345, 131)
        self.save_button.clicked.connect(self.create_room)

    def clear_form(self) -> None:
        self.rows_box.setValue(0)
        self.cols_box.setValue(0)
        self.feedback_label.clear()
        self.cinema_box.setValue(0)

    def create_room(self) -> None:
        rows_cnt = self.rows_box.value()
        cols_cnt = self.cols_box.value()
        cinema_id = self.cinema_box.value()
        cinema = cursor.execute(f"SELECT id from cinemas WHERE id={cinema_id}").fetchall()
        if cols_cnt and cinema_id and len(cinema) and rows_cnt:
            cursor.execute(f"INSERT INTO rooms(cinema, rows, cols) "
                           f"VALUES ({cinema_id}, {rows_cnt}, {cols_cnt})")
            connection.commit()
            all_rooms.load_rooms_data()
            self.close()
        else:
            self.feedback_label.setText("Неверно заполнена форма")

    def closeEvent(self, event) -> None:
        self.clear_form()


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


class CreateReport(QWidget, Ui_CreateReport):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(241, 130)
        self.initUI()

    def initUI(self):
        self.dir_name = None
        self.save_report_button.clicked.connect(self.create_report_query)
        connection.create_function("CHECK_DATETIME", 1, self.check_data)
        self.base_query = "SELECT films.price, films.datetime " \
                          "FROM films " \
                          "INNER JOIN cheques ON cheques.film=films.id " \
                          "WHERE CHECK_DATETIME(films.datetime) = 1 "
        self.create_months_dicts()

    def create_months_dicts(self) -> None:
        self.num_to_month = {1: "Январь", 2: "Февраль", 3: "Март",
                             4: "Апрель", 5: "Май", 6: "Июнь",
                             7: "Июль", 8: "Август", 9: "Сентябрь",
                             10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
        self.month_with_sums = defaultdict(lambda: 0)

    @staticmethod
    def check_data(datetime: str) -> int:
        """
        cheches if film's year is equal to current year
        """
        if dt.datetime(*map(int, datetime.split())).year == dt.datetime.now().year:
            return 1
        return 0

    def create_report_query(self) -> None:
        cinemas = self.cinema_labels.text().lower()
        query = self.base_query
        query_true = False

        if cinemas != "все":
            try:
                cinemas = list(map(int, cinemas.split()))
            except Exception:
                self.feedback_label.setText("Неверно заполнена форма")
                return
            query = self.base_query + 'and films.cinema IN (' + ', '.join([str(i) for i in cinemas]) + ')'
            query_true = True
        if cinemas != "все" and not query_true:
            self.feedback_label.setText("Неверно заполнена форма")
            return

        query_result = cursor.execute(query).fetchall()
        self.create_report(query_result)
        self.close()

    def create_report(self, query_result: list) -> None:
        for price, datetime in query_result:
            month = dt.datetime(*map(int, datetime.split())).month
            self.month_with_sums[self.num_to_month[month]] += price

        if not any(self.month_with_sums.values()):
            QMessageBox.warning(self, "Отчет", "За этот год покупок не было",
                                QMessageBox.Ok)
            return

        datetime = self.create_csv_table()
        self.create_circle_graphic()
        self.create_months_dicts()
        QMessageBox.warning(self, "Отчет", f"Отчет находится в: {self.dir_name}",
                            QMessageBox.Ok)
        cursor.execute("INSERT INTO reports(path, datetime) VALUES(?, ?)", (self.dir_name, datetime))
        connection.commit()
        all_reports.load_report_data()

    def create_csv_table(self) -> str:
        datetime = dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.dir_name = 'data/reports/report_' + datetime + '/'
        os.makedirs(self.dir_name)
        with open(self.dir_name + 'table.csv', "w", newline='', encoding="utf-8") as report_csv:
            writer = csv.writer(report_csv, delimiter=';', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Месяц", "Доход"])
            for month in self.num_to_month.values():
                row = [month, self.month_with_sums[month]]
                writer.writerow(row)
        return datetime

    def create_circle_graphic(self) -> None:
        labels = [month for month in self.num_to_month.values() if self.month_with_sums[month]]
        values = [self.month_with_sums[month] for month in labels]
        figure, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.axis("equal")
        ax.legend(loc='upper left', bbox_to_anchor=(0.87, 1.0))
        plt.savefig(self.dir_name + 'graphic.png')


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

    def fill(self, film_id: int, price: int) -> None:
        self.user_id = int(user_profile.user_id_edit.text())
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
                user_profile.load_cheques_data(self.user_id)
                user_profile.total_money_edit.setText(str(int(user_profile.total_money_edit.text()) + self.price))
                self.create_text_cheque(cheque_id,
                                        dt.datetime.now().strftime("%Y.%m.%d %H:%M"),
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
                         f"Начало фильма: {dt.datetime(*map(int, film_data[3].split())).strftime('%Y.%m.%d %H:%M')}\n"
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


class ChequeView(QWidget, Ui_ChequeView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(322, 362)

    def fill(self, filename: str):
        if not os.path.isfile(filename):
            QMessageBox.critical(self, "Чек", "Файл не найден",
                                 QMessageBox.Ok)
            return

        with open(filename, encoding="utf-8") as cheque:
            data = cheque.readlines()
            self.film_name_edit.setText(data[2][data[2].find(': ') + 2:])
            self.cinema_name_edit.setText(data[3][data[3].find(': ') + 2:])
            self.room_id_edit.setText(data[4][data[4].find(': ') + 2:])
            self.film_start_edit.setText(data[5][data[5].find(': ') + 2:])
            self.cheque_id_edit.setText(data[6][data[6].find(': ') + 2:])
            self.unique_key_edit.setText(data[7][data[7].find(': ') + 2:])
            self.buy_time_edit.setText(data[8][data[8].find(': ') + 2:])
            self.row_edit.setText(data[9][data[9].find(': ') + 2:data[9].find(',')])
            self.col_edit.setText(data[9][data[9].rfind(': ') + 2:])
            self.total_edit.setText(data[10][data[10].find(': ') + 2:])
        self.show()


class ReportView(QWidget, Ui_ReportView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(662, 866)

    def fill(self, dir_name: str) -> None:
        pixmap = QPixmap(dir_name + "/graphic.png")
        self.image.setPixmap(pixmap)
        table_data = list()
        with open(dir_name + 'table.csv', encoding="utf-8") as csvtable:
            reader = csv.reader(csvtable, delimiter=';', quoting=csv.QUOTE_NONE)
            next(reader)
            for row in reader:
                if int(row[1]):
                    table_data.append((row[0], row[1]))
        create_table(["Месяц", "Доход"], table_data, self.months_table_data)
        self.show()


class UserFilms(QWidget, Ui_UserFilms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self) -> None:
        self.room = RoomView()
        self.search_button.clicked.connect(self.search)
        self.afisha_button.clicked.connect(self.watch_afisha)
        self.buy_ticket_button.clicked.connect(self.watch_room)
        self.search_by_box.addItem("Нет")
        self.search_by_box.addItem("Кинотеатр")
        self.search_by_box.addItem("Название")
        self.search_by_box.addItem("Жанр")
        self.search_by_box.addItem("Максимальная цена")
        self.base_query = f"SELECT films.id, films.name, genres.name, films.duration, " \
                          f"films.datetime, cinemas.name, rooms.id, films.price FROM " \
                          f"films INNER JOIN genres ON genres.id = films.genre INNER " \
                          f"JOIN cinemas ON cinemas.id = films.cinema INNER JOIN rooms " \
                          f"ON rooms.id = films.room WHERE films.can_buy = 1 "
        self.query = self.base_query[:]
        self.order = " ORDER BY films.datetime"
        self.load_films_data()

    def search(self) -> None:
        search_by = self.search_by_box.currentText()
        search_text = self.search_edit.text()

        if search_by == 'Нет':
            self.query = self.base_query[:]

        if search_text:
            if search_by == "Кинотеатр":
                self.query = self.base_query + f" and cinemas.name LIKE '%{search_text}%'"
            elif search_by == "Название":
                self.query = self.base_query + f" and films.name LIKE '%{search_text}%'"
            elif search_by == "Жанр":
                self.query = self.base_query + f" and genres.name LIKE '%{search_text}%'"
            elif search_by == "Максимальная цена" and search_text.isdigit():
                self.query = self.base_query + f" and films.price <= {int(search_text)}"
            self.load_films_data()

    def load_films_data(self) -> None:
        query_result = cursor.execute(self.query + self.order).fetchall()

        if query_result:
            titles = ["ИД", "Название фильма", "Жанр", "Продолжительность", "Начало", "Кинотеатр", "Зал", "Цена"]
            create_table(titles, query_result, self.films_table_data)
        else:
            self.clear_table()

    def watch_afisha(self) -> None:
        row = self.films_table_data.currentRow()
        if row == -1:
            return

        film_id = int(self.films_table_data.item(row, 0).text())
        afisha = cursor.execute("SELECT films.name, genres.name, descriptions.description, "
                                "descriptions.image "
                                "FROM descriptions "
                                f"INNER JOIN films ON films.afisha = descriptions.id and films.id = {film_id} "
                                f"INNER JOIN genres ON genres.id = films.genre").fetchone()
        if afisha:
            afisha_view.fill(*afisha)
            afisha_view.show()
        else:
            QMessageBox.warning(
                self, 'Афиша', "На этот фильм еще нет афиши",
                QMessageBox.Ok)

    def watch_room(self):
        row = self.films_table_data.currentRow()
        if row == -1:
            return
        film_id = int(self.films_table_data.item(row, 0).text())
        price = int(self.films_table_data.item(row, 7).text())

        self.room.fill(film_id, price)
        self.room.show()

    def clear_table(self) -> None:
        while self.films_table_data.rowCount():
            self.films_table_data.removeRow(0)


class UserProfile(QWidget, Ui_UserProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def fill(self, user_id: int) -> None:
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
            create_table(titles, query_result, self.purchase_table_data)

    def watch_cheque(self):
        row = self.purchase_table_data.currentRow()
        if row == -1:
            return

        filename = 'data/cheques/cheque_' + self.purchase_table_data.item(row, 0).text()
        self.cheque_view.fill(filename)


class AllFilms(QWidget, Ui_AllFilms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(710)
        self.create_afisha_form = CreateAfisha()
        self.initUI()

    def initUI(self) -> None:
        self.add_film_button.clicked.connect(self.add_film)
        self.delete_film_button.clicked.connect(self.delete_film)
        self.create_afisha_button.clicked.connect(self.create_afisha)
        self.load_film_data()

    def create_afisha(self) -> None:
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        film_name = self.film_table_data.item(row, 1).text()
        genre_id, afisha_id = cursor.execute(f"SELECT genres.id, films.afisha "
                                             f"FROM films "
                                             f"INNER JOIN genres ON genres.id = films.genre "
                                             f"WHERE films.name='{film_name}'").fetchone()
        if afisha_id:
            valid = QMessageBox.question(self, "Афиша",
                                         "У данного фильма уже есть афиша, удалить и перезаписать?",
                                         QMessageBox.Yes, QMessageBox.No)
            if valid != QMessageBox.Yes:
                return
            cursor.execute(f"UPDATE films SET afisha=NULL WHERE name=? and genre={genre_id}", (film_name, ))
            cursor.execute(f"DELETE FROM descriptions WHERE id={afisha_id}")
            connection.commit()

        self.create_afisha_form.film_name = film_name
        self.create_afisha_form.genre_id = genre_id
        self.create_afisha_form.show()

    def load_film_data(self) -> None:
        query_result = cursor.execute(f"SELECT "
                                      f"films.id, films.name, genres.name, films.duration, "
                                      f"films.datetime, cinemas.name, rooms.id, films.price "
                                      f"FROM films "
                                      f"INNER JOIN genres ON genres.id = films.genre "
                                      f"INNER JOIN cinemas ON cinemas.id = films.cinema "
                                      f"INNER JOIN rooms ON rooms.id = films.room "
                                      f"WHERE films.can_buy = 1 "
                                      f"ORDER BY films.name;").fetchall()

        if query_result:
            titles = ["ИД", "Название фильма", "Жанр", "Продолжительность", "Начало", "Кинотеатр", "Зал", "Цена"]
            create_table(titles, query_result, self.film_table_data)
        else:
            self.clear_table()

    def clear_table(self) -> None:
        while self.film_table_data.rowCount() > 0:
            self.film_table_data.removeRow(0)

    @staticmethod
    def add_film() -> None:
        create_film.setWindowTitle("Добавление фильма")
        create_film.show()

    def delete_film(self) -> None:
        row = self.film_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный фильм?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            film_id = int(self.film_table_data.item(row, 0).text())
            cursor.executescript(f"UPDATE films SET can_buy = 0 WHERE id={film_id}; "
                                 f"DELETE FROM seats WHERE film={film_id}")
            connection.commit()
            self.load_film_data()


class AllGenres(QWidget, Ui_AllGenres):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(710)
        self.initUI()

    def initUI(self) -> None:
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
                create_film.create_genres_box()
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
                    create_film.create_genres_box()
                else:
                    QMessageBox.critical(self, "Ошибка",
                                         "Неверно заполнена форма")

    def delete_genre(self) -> None:
        row = self.genre_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный жанр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            genre_id = int(self.genre_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE genre={genre_id}; "
                                 f"DELETE FROM genres WHERE id={genre_id}")
            connection.commit()
            self.load_genre_data()
            create_film.create_genre_box()


class AllCinemas(QWidget, Ui_AllCinemas):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.report = CreateReport()
        self.setFixedWidth(711)
        self.initUI()

    def initUI(self) -> None:
        self.add_cinema_button.clicked.connect(self.add_cinema)
        self.delete_cinema_button.clicked.connect(self.delete_cinema)
        self.report_button.clicked.connect(self.create_report)
        self.load_cinema_data()

    def create_report(self):
        self.report.show()

    def load_cinema_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM cinemas").fetchall()

        if query_result:
            titles = ["ID", "Имя"]
            create_table(titles, query_result, self.cinema_table_data)
        else:
            self.clear_table()

    def add_cinema(self) -> None:
        name, ok_pressed = QInputDialog.getText(self, "Кинотеатр",
                                                "Введите имя нового кинотеатра")
        if ok_pressed:
            if name:
                cursor.execute(f"INSERT INTO cinemas(name) "
                               f"VALUES (?)", (name,))
                connection.commit()
                self.load_cinema_data()
            else:
                QMessageBox.critical(self, "Ошибка",
                                     "Неверно заполнена форма")

    def clear_table(self) -> None:
        while self.cinema_table_data.rowCount() > 0:
            self.cinema_table_data.removeRow(0)

    def delete_cinema(self) -> None:
        row = self.cinema_table_data.currentRow()
        if row == -1:
            return

        valid = QMessageBox.question(
                self, '', "Действительно удалить данный кинотеатр?",
                QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cinema_id = int(self.cinema_table_data.item(row, 0).text())
            cursor.executescript(f"DELETE FROM films WHERE cinema={cinema_id}; "
                                 f"DELETE FROM rooms WHERE cinema={cinema_id}; "
                                 f"DELETE FROM cinemas WHERE id={cinema_id}")
            connection.commit()
            self.load_cinema_data()
            all_films.load_film_data()
            all_rooms.load_rooms_data()


class AllRooms(QWidget, Ui_AllRooms):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_room = CreateRoom()
        self.initUI()

    def initUI(self) -> None:
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
            all_films.load_film_data()


class AllUsers(QWidget, Ui_AllUsers):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_users_data()

    def load_users_data(self) -> None:
        query_result = cursor.execute(f"SELECT * FROM users").fetchall()
        titles = ["ID", "Имя", "Пароль", "Админ", "Сумма покупок"]
        create_table(titles, query_result, self.users_table_data, enable=True)


class AllReports(QWidget, Ui_AllReports):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.report_view = ReportView()
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
        self.report_view.fill(dir_name)

    def load_report_data(self):
        query_result = cursor.execute("SELECT * FROM reports").fetchall()
        if query_result:
            titles = ["ID", "Путь к файлу", "Время создания"]
            create_table(titles, query_result, self.reports_table_data)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    user_profile, all_cinemas = None, None
    all_films, all_genres = None, None
    all_rooms, create_film = None, None
    main_admin_window, user_main_window = None, None
    afisha_view, user_films = None, None
    all_reports = None
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    login_window = LoginWindow()
    register_window = RegisterWindow()
    login_window.show()
    sys.exit(app.exec_())
