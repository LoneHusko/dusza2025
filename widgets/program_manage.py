import sys, os, ctypes

from PySide6.QtGui import Qt, QPalette, QColor, QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, \
    QStyleFactory, QHBoxLayout, QFileDialog, QListWidget, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QMessageBox, \
    QProgressBar
from pyexpat.errors import messages

from modules.models import State, Computer

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class StopProgram(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path
        self.cluster = State().read_from_path(cluster_path)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Program leállítása</h1>"))

        self.running_processes = QListWidget()
        self.layout.addWidget(self.running_processes)
        self.running_processes.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.update_list()

        self.stop_button = QPushButton("Leállítás")
        self.layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop)

    def update_list(self):
        self.running_processes.clear()
        self.cluster = State().read_from_path(self.cluster_path)
        for i, program in enumerate(self.cluster.cluster_processes):
            self.running_processes.addItem(f"{i}: {program.name}")

    def stop(self):
        messages = []
        for i in self.running_processes.selectedItems():
            choice = int(i.text().split(":")[0])
            chosen_program = self.cluster.cluster_processes[choice]
            self.cluster.cluster_processes.remove(chosen_program)

            for computer in self.cluster.computers:
                computer.processes = [i for i in computer.processes if i.name != chosen_program.name]

            self.cluster.write_to_path(self.cluster_path)
            messages.append(f"{chosen_program.name} sikeresen leállítva!")

        QMessageBox.information(
            self,
            "Sikeres művelet",
            "\n".join(messages),
        )
        self.update_list()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(QPalette(QColor("#2b2d30")))
    window = StopProgram()
    window.show()
    app.exec()
