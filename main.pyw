import ctypes
import sys
from queue import Queue

from PySide6 import QtCore
from PySide6.QtCore import QMetaObject, QObject, Slot
from PySide6.QtGui import Qt, QPalette, QColor
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QStyleFactory, QHBoxLayout, \
    QFileDialog, QFrame, QMessageBox

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
    invoker.invoke(func, *args, **kwargs)


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

        self.sidebar = QFrame(self)
        self.sidebar.setStyleSheet("QFrame{background-color: #1e1f22; border-radius: 5px}")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.sidebar.setFixedWidth(200 * scaleFactor)
        self.sidebar.setLayout(self.sidebar_layout)
        self.central_layout.addWidget(self.sidebar)

        for i in widgets.keys():
            self.central_layout.addWidget(widgets[i])
            widgets[i].setVisible(False)

        self.computer_add_button = QPushButton("Számítógép hozzáadása")
        self.computer_add_button.clicked.connect(lambda: self.switch_widget("computer.add", self.computer_add_button))
        self.sidebar_layout.addWidget(self.computer_add_button)

        self.computer_remove_button = QPushButton("Számítógép törlése")
        self.computer_remove_button.clicked.connect(
            lambda: self.switch_widget("computer.delete", self.computer_remove_button))
        self.sidebar_layout.addWidget(self.computer_remove_button)

        self.program_stop_button = QPushButton("Program végleges leállítása")
        self.program_stop_button.clicked.connect(lambda: self.switch_widget("program.stop", self.program_stop_button))
        self.sidebar_layout.addWidget(self.program_stop_button)

        self.program_edit_button = QPushButton("Program módosítása")
        self.program_edit_button.clicked.connect(lambda: self.switch_widget("program.edit", self.program_edit_button))
        self.sidebar_layout.addWidget(self.program_edit_button)

        self.program_start_button = QPushButton("Új folyamat")
        self.program_start_button.clicked.connect(lambda: self.switch_widget("program.run", self.program_start_button))
        self.sidebar_layout.addWidget(self.program_start_button)

    def switch_widget(self, widget_name, obj):
        children = []
        for i in range(self.sidebar_layout.count()):
            child = self.sidebar_layout.itemAt(i).widget()
            if child:
                children.append(child)
        for child in children:
            child.setStyleSheet("font-weight: initial")
        obj.setStyleSheet("font-weight: bold")
        for i in widgets.keys():
            widgets[i].setVisible(False)
        widgets[widget_name].setVisible(True)
        widgets[widget_name].update_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(QPalette(QColor("#2b2d30")))
    cluster_path = QFileDialog.getExistingDirectory(caption="Válaszd ki a klaszter mappát")

    if not cluster_path:
        QMessageBox.critical(
            None,
            "Hiba",
            "Nincs klaszter kiválasztva"
        )
        sys.exit(1)

    from widgets import computer_manage, program_manage

    widgets: {str, QWidget} = {
        "computer.add": computer_manage.ComputerAdd(cluster_path),
        "computer.delete": computer_manage.ComputerRemove(cluster_path),
        "program.stop": program_manage.StopProgram(cluster_path),
        "program.edit": program_manage.EditProgram(cluster_path),
        "program.run": program_manage.RunProgram(cluster_path),
    }

    window = MainWindow()
    window.show()
    app.exec()
