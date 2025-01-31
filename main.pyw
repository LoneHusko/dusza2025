import sys
import ctypes
import json
import os.path
import time
import traceback
from threading import Thread
from queue import Queue
import subprocess
from PySide6 import QtCore
from PySide6.QtCore import QMetaObject, QObject, Slot
from PySide6.QtGui import Qt, QPalette, QColor, QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, \
    QStyleFactory, QHBoxLayout, QFileDialog, QListWidget, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QMessageBox, \
    QProgressBar

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class Invoker(QObject):
    def __init__(self):
        super(Invoker, self).__init__()
        self.queue = Queue()

    def invoke(self, func, *args, **kwargs):
        f = lambda: func(*args, **kwargs)
        self.queue.put(f)
        # noinspection PyTypeChecker
        QMetaObject.invokeMethod(self, "handler", QtCore.Qt.QueuedConnection)

    @Slot()
    def handler(self):
        f = self.queue.get()
        f()


invoker = Invoker()


def invoke_in_main_thread(func, *args, **kwargs):
    invoker.invoke(func,*args, **kwargs)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dusza2025")
        self.setStyleSheet("font-size: 16px")
        self.setFixedSize(720 * scaleFactor, 480 * scaleFactor)
        self.central_widget = QWidget(self)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)
        self.central_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.sidebar = QWidget(self)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sidebar.setFixedWidth(200 * scaleFactor)
        self.sidebar.setLayout(self.sidebar_layout)
        self.central_layout.addWidget(self.sidebar)

        for i in widgets.keys():
            self.central_layout.addWidget(widgets[i])
            widgets[i].setVisible(False)

        self.computer_add_button = QPushButton("Számítógép hozzáadása")
        self.computer_add_button.clicked.connect(lambda: self.switch_widget("computer.add"))
        self.sidebar_layout.addWidget(self.computer_add_button)

        self.computer_remove_button = QPushButton("Számítógép törlése")
        self.computer_remove_button.clicked.connect(lambda: self.switch_widget("computer.delete"))
        self.sidebar_layout.addWidget(self.computer_remove_button)

    def switch_widget(self, widget_name):
        for i in widgets.keys():
            widgets[i].setVisible(False)
        widgets[widget_name].setVisible(True)
        if widget_name == "computer.delete":
            widgets[widget_name].update_list()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(QPalette(QColor("#2b2d30")))
    cluster_path = QFileDialog.getExistingDirectory(caption="Válaszd ki a klaszter mappát")

    from widgets import computer_manage
    widgets: {str, QWidget} = {
        "computer.add": computer_manage.ComputerAdd(cluster_path),
        "computer.delete": computer_manage.ComputerRemove(cluster_path),
    }

    window = MainWindow()
    window.show()
    app.exec()