import os
import sqlite3
import sys

from time import sleep, monotonic
from datetime import timedelta
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QAction

with open('StyleSheet.css', 'r') as file:
    StyleSheet = file.read()

count = 0


def code_interpreter(code: str, time_d: int):
    test_file = open('tmp_test_file.py', 'w', encoding='utf-8')
    test_file.write(r'''import sys
with open("in.txt", "r") as in_file:
    inputs_str = in_file.read().split('\n')
out_file = open("out.txt", "w", encoding="utf-8")

tmp_print = print
global_inp_counter = -1


def input():
    global global_inp_counter, inputs_str
    global_inp_counter += 1
    if global_inp_counter > len(inputs_str) - 1:
        raise IndexError('No more inputs')
    return inputs_str[global_inp_counter]


def print(*args, **kargs):
    if "file" in kargs:
        kargs['file'] = out_file
    else:
        kargs.update({'file': out_file})
    tmp_print(*args, **kargs)
try:''')
    code = '\n' + code
    for i in code.split('\n'):
        test_file.write('    ' + i + '\n')

    test_file.write(r'''except Exception as ex:
    with open("out.txt", "w", encoding="utf-8") as f:
        f.write('!Exception!\n')
        f.write(str(ex.__class__.__name__) + '\n')
        f.write('\n'.join(ex.args))
out_file.close()''')
    test_file.close()
    with open('out.txt', 'w', encoding='utf-8')as f:
        f.write('Не удалось выполнить код\n    :(')
    os.startfile('tmp_test_file.py')
    sleep(time_d)
    with open('out.txt', 'r', encoding='utf-8')as f:
        return f.read().strip()  # .split('\n')


def check_answer(answer: str, correct_answer: str) -> str:
    if answer == correct_answer:
        return 'ok'
    if len(answer.split()) != len(correct_answer.split()):
        return f'Одидалось строк: {len(correct_answer.split())}\nПолучено строк: {len(answer.split())}'
    for a, c_a in zip(answer.split(), correct_answer.split()):
        if a != c_a:
            return f'Строка {answer.split().index(a) + 1}:\n\tОжидалось: {c_a}\n\tПолучено: {a}'


def output_of_symbols_by_symbol(label: QtWidgets.QLabel, text: str) -> None:
    global count
    count = 0

    def tmp():
        global count
        label.setText(label.text() + text[count])
        count += 1

    def pas():
        global count
        count += 1

    def rem():
        global count
        label.setText(label.text()[:-1])
        count += 1

    for j in enumerate(text):
        if j[1] != '&' and j[1] != '$':
            QTimer.singleShot(80 * j[0], lambda: tmp())
        elif j[1] == '$':
            QTimer.singleShot(80 * j[0], lambda: rem())
        else:
            QTimer.singleShot(80 * j[0], lambda: pas())


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.count_task_id = 0
        self.data_base = sqlite3.connect('data.db')

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(747, 545)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.task_label = QtWidgets.QScrollArea(self.groupBox_2)
        self.task_label.setWidgetResizable(True)
        self.task_label.setObjectName("task_label")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 333, 303))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.task_label.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.addWidget(self.task_label)
        self.start_code = QtWidgets.QPushButton(self.groupBox_2)
        self.start_code.setObjectName("start_code")
        self.verticalLayout_4.addWidget(self.start_code)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.code_load_main = QtWidgets.QToolBox(self.groupBox)
        self.code_load_main.setAcceptDrops(True)
        self.code_load_main.setObjectName("code_load_main")
        self.file_load = QtWidgets.QWidget()
        self.file_load.setGeometry(QtCore.QRect(0, 0, 335, 278))
        self.file_load.setObjectName("file_load")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.file_load)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_file_bth = QtWidgets.QPushButton(self.file_load)
        self.select_file_bth.setObjectName("select_file_bth")
        self.horizontalLayout.addWidget(self.select_file_bth)
        self.file_name = QtWidgets.QLabel(self.file_load)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name.sizePolicy().hasHeightForWidth())
        self.file_name.setSizePolicy(sizePolicy)
        self.file_name.setObjectName("file_name")
        self.horizontalLayout.addWidget(self.file_name)
        self.code_load_main.addItem(self.file_load, "")
        self.text_load = QtWidgets.QWidget()
        self.text_load.setGeometry(QtCore.QRect(0, 0, 335, 278))
        self.text_load.setObjectName("text_load")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.text_load)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.code_plane_edit = QtWidgets.QPlainTextEdit(self.text_load)
        self.code_plane_edit.setObjectName("code_plane_edit")
        self.verticalLayout_3.addWidget(self.code_plane_edit)
        self.code_load_main.addItem(self.text_load, "")
        self.verticalLayout_2.addWidget(self.code_load_main)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.log_box = QtWidgets.QGroupBox(self.centralwidget)
        self.log_box.setObjectName("log_box")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.log_box)
        self.verticalLayout.setObjectName("verticalLayout")
        self.log_output = QtWidgets.QLabel(self.log_box)
        self.log_output.setText("")
        self.log_output.setObjectName("log_output")
        self.verticalLayout.addWidget(self.log_output)
        self.lineEdit = QtWidgets.QLineEdit(self.log_box)
        self.lineEdit.setFrame(False)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.gridLayout.addWidget(self.log_box, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 747, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.setting = QtWidgets.QMenu(self.menu)
        self.setting.setObjectName("setting")
        self.tasks_menu = QtWidgets.QMenu(self.menubar)
        self.tasks_menu.setObjectName("tasks_menu")
        self.st_menu = QtWidgets.QMenu(self.menubar)
        self.st_menu.setObjectName("st_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.save = QtWidgets.QAction(MainWindow)
        self.save.setObjectName("save")
        self.load = QtWidgets.QAction(MainWindow)
        self.load.setObjectName("load")
        self.statistic = QtWidgets.QAction(MainWindow)
        self.statistic.setObjectName("statistic")
        self.abought_us = QtWidgets.QAction(MainWindow)
        self.abought_us.setObjectName("abought_us")
        self.sinbhol_out = QtWidgets.QAction(MainWindow)

        self.sinbhol_out.setObjectName("sinbhol_out")
        self.task_1 = QtWidgets.QAction(MainWindow)

        self.task_1.setObjectName("task_1")
        self.task_2 = QtWidgets.QAction(MainWindow)

        self.task_2.setObjectName("task_2")
        self.task_3 = QtWidgets.QAction(MainWindow)

        self.task_3.setObjectName("task_3")
        self.task_4 = QtWidgets.QAction(MainWindow)

        self.task_4.setObjectName("task_4")
        self.task_5 = QtWidgets.QAction(MainWindow)

        self.task_5.setObjectName("task_5")
        self.actionpass = QtWidgets.QAction(MainWindow)
        self.actionpass.setObjectName("actionpass")
        self.action = QtWidgets.QAction(MainWindow)

        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)

        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)

        self.action_3.setObjectName("action_3")
        self.action_4 = QtWidgets.QAction(MainWindow)

        self.action_4.setObjectName("action_4")
        self.action_5 = QtWidgets.QAction(MainWindow)

        self.action_5.setObjectName("action_5")
        self.action_6 = QtWidgets.QAction(MainWindow)

        self.action_6.setObjectName("action_6")
        self.action_7 = QtWidgets.QAction(MainWindow)

        self.action_7.setObjectName("action_7")
        self.action_8 = QtWidgets.QAction(MainWindow)

        self.action_8.setObjectName("action_8")
        self.action_9 = QtWidgets.QAction(MainWindow)

        self.action_9.setObjectName("action_9")
        self.action_10 = QtWidgets.QAction(MainWindow)

        self.action_10.setObjectName("action_10")
        self.setting.addAction(self.sinbhol_out)
        self.menu.addAction(self.statistic)
        self.menu.addAction(self.setting.menuAction())
        self.tasks_menu.addAction(self.task_1)
        self.tasks_menu.addAction(self.task_2)
        self.tasks_menu.addAction(self.task_3)
        self.tasks_menu.addAction(self.task_4)
        self.tasks_menu.addAction(self.task_5)
        self.st_menu.addAction(self.action)
        self.st_menu.addAction(self.action_2)
        self.st_menu.addAction(self.action_3)
        self.st_menu.addAction(self.action_4)
        self.st_menu.addAction(self.action_5)
        self.st_menu.addAction(self.action_6)
        self.st_menu.addAction(self.action_7)
        self.st_menu.addAction(self.action_8)
        self.st_menu.addAction(self.action_9)
        self.st_menu.addAction(self.action_10)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.tasks_menu.menuAction())
        self.menubar.addAction(self.st_menu.menuAction())

        self.retranslateUi(MainWindow)
        self.code_load_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.load_task(0)
        self.code_plane_edit.setPlaceholderText('Введите код...')
        self.start_code.clicked.connect(self.code_intp)
        self.select_file_bth.clicked.connect(self.o_file)

        self.code_plane_edit.textChanged.connect(self.c_file)
        self.sinbhol_out.changed.connect(self.out_s_c)
        self.sinbhol_out.setCheckable(True)
        self.sinbhol_out.setChecked(True)
        self.is_sinbhol_out = True

        self.task_1.triggered.connect(self.t_sel)
        self.task_2.triggered.connect(self.t_sel)
        self.task_3.triggered.connect(self.t_sel)
        self.task_4.triggered.connect(self.t_sel)
        self.task_5.triggered.connect(self.t_sel)

        self.action.triggered.connect(self.change_stud)
        self.action_2.triggered.connect(self.change_stud)
        self.action_3.triggered.connect(self.change_stud)
        self.action_4.triggered.connect(self.change_stud)
        self.action_5.triggered.connect(self.change_stud)
        self.action_6.triggered.connect(self.change_stud)
        self.action_7.triggered.connect(self.change_stud)
        self.action_8.triggered.connect(self.change_stud)
        self.action_9.triggered.connect(self.change_stud)
        self.action_10.triggered.connect(self.change_stud)

        self.n_task = None
        self.n_stud = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Задание"))
        self.start_code.setText(_translate("MainWindow", "Запустить код"))
        self.groupBox.setTitle(_translate("MainWindow", "Код"))
        self.select_file_bth.setText(_translate("MainWindow", "Загрузить файл"))
        self.file_name.setText(_translate("MainWindow", "Файл не загружен"))
        self.code_load_main.setItemText(self.code_load_main.indexOf(self.file_load),
                                        _translate("MainWindow", "Загрузить файл"))
        self.code_load_main.setItemText(self.code_load_main.indexOf(self.text_load),
                                        _translate("MainWindow", "Редактировать код"))
        self.log_box.setTitle(_translate("MainWindow", "Лог"))
        self.lineEdit.setText(_translate("MainWindow", "лпокплоклп\\nffrekf"))
        self.menu.setTitle(_translate("MainWindow", "Меню"))
        self.setting.setTitle(_translate("MainWindow", "Настройки"))
        self.tasks_menu.setTitle(_translate("MainWindow", "Задачи"))
        self.st_menu.setTitle(_translate("MainWindow", "Ученики"))
        self.save.setText(_translate("MainWindow", "Сохранить"))
        self.load.setText(_translate("MainWindow", "Загрузить"))
        self.statistic.setText(_translate("MainWindow", "Статистика"))
        self.abought_us.setText(_translate("MainWindow", "Об авторе"))
        self.sinbhol_out.setText(_translate("MainWindow", "Посимвольный вывод"))
        self.task_1.setText(_translate("MainWindow", "Задача 1"))
        self.task_2.setText(_translate("MainWindow", "Задача 2"))
        self.task_3.setText(_translate("MainWindow", "Задача 3"))
        self.task_4.setText(_translate("MainWindow", "Задача 4"))
        self.task_5.setText(_translate("MainWindow", "Задача 5"))
        self.actionpass.setText(_translate("MainWindow", "pass"))
        self.action.setText(_translate("MainWindow", "Албычев Дмитрий"))
        self.action_2.setText(_translate("MainWindow", "Базалевский Омар"))
        self.action_3.setText(_translate("MainWindow", "Бубликова Анна"))
        self.action_4.setText(_translate("MainWindow", "Егиян Давид"))
        self.action_5.setText(_translate("MainWindow", "Карпец Екатерина"))
        self.action_6.setText(_translate("MainWindow", "Никифоров Артемий"))
        self.action_7.setText(_translate("MainWindow", "Петифорова Анастасия"))
        self.action_8.setText(_translate("MainWindow", "Петухов Дмитрий"))
        self.action_9.setText(_translate("MainWindow", "Полубатько Владислава"))
        self.action_10.setText(_translate("MainWindow", "Потапова Алиса"))

    def o_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Python Code(*.py)")
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.code_plane_edit.setPlainText(f.read())
            self.file_name.setText(f"<b>{filename}</b>")

    def c_file(self):
        self.file_name.setText("Файл не загружен")

    def out_s_c(self):
        self.is_sinbhol_out = self.sinbhol_out.isChecked()

    def change_stud_f(self, id):
        print(id)

    def change_stud(self):
        st_list = ['Албычев Дмитрий', 'Базалевский Омар', 'Бубликова Анна', 'Егиян Давид', 'Карпец Екатерина',
                   'Никифоров Артемий', 'Петифорова Анастасия', 'Петухов Дмитрий', 'Полубатько Владислава',
                   'Потапова Алиса']
        self.change_stud_f(st_list.index(self.sender().text()))

    def t_sel(self):
        print(self.sender().text())
        self.load_task_f(int(self.sender().text()[7:]))

    def load_task_f(self, num):
        print('LOADING...', num)

    def code_intp(self):
        if self.n_task == None:
            pass
        self.start_code.setEnabled(False)
        ready = code_interpreter(self.code_plane_edit.toPlainText(), 1)
        QTimer.singleShot(1100, lambda: self.start_code.setEnabled(True))
        if self.is_sinbhol_out:
            output_of_symbols_by_symbol(self.log_output, '--==[Вердикт]==----------\n' + ready + '\n----------------')
        else:
            self.log_output.setText(self.log_output.text() + ready + '\n')

    def load_task(self, id):
        try:
            cur = self.data_base.cursor()
            '''
            for i in range(10):
                a = input().split()
                data = (int(a[0]), ' '.join(a[1:]))
                cur.execute("INSERT INTO general_types VALUES(?, ?);", data)'''
            # a = cur.execute('SELECT * FROM tasks WHERE id = ' + str(id))

            # print(*a)
            # self.lvl_base.commit()

            # self.lvl_base.close()
        except Exception as ex:
            print(ex)


class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


app = QApplication(sys.argv)
app.setStyleSheet(StyleSheet)
ex = Main_window()
ex.show()
sys.exit(app.exec_())
