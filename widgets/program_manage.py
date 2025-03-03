import ctypes
import datetime
import random
import string
import sys

from PySide6.QtCore import QAbstractItemModel
from PySide6.QtGui import Qt, QPalette, QColor, QIntValidator
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QComboBox, QLabel, \
    QStyleFactory, QListWidget, QFrame, QLineEdit, QMessageBox, QCompleter, QWidget, QScrollArea, QSplitter

from modules.models import State, ProcessState

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class StopProgram(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path
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
        cluster = State().read_from_path(self.cluster_path)
        for i, program in enumerate(cluster.cluster_processes):
            self.running_processes.addItem(f"{program.name}")

    def stop(self):
        messages = []
        cluster = State().read_from_path(self.cluster_path)
        for i in self.running_processes.selectedItems():
            chosen_program = [i.name for i in cluster.cluster_processes if i.name == i.text()][0]
            cluster.cluster_processes.remove(chosen_program)

            for computer in cluster.computers:
                computer.processes = [i for i in computer.processes if i.name != chosen_program.name]

            cluster.write_to_path(self.cluster_path)
            messages.append(f"{chosen_program.name} sikeresen leállítva!")

        QMessageBox.information(
            self,
            "Sikeres művelet",
            "\n".join(messages),
        )
        self.update_list()


class EditProgram(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Program módosítása</h1>"))

        self.program_list = QComboBox()
        self.layout.addWidget(self.program_list)
        self.program_list.currentIndexChanged.connect(self.set_values)

        self.layout.addWidget(QLabel("Futtatandó példányok"))
        self.program_count = QLineEdit(self)
        self.program_count.setValidator(QIntValidator())
        self.layout.addWidget(self.program_count)

        self.layout.addWidget(QLabel("Processzorigény (millimag)"))
        self.processor = QLineEdit(self)
        self.processor.setValidator(QIntValidator())
        self.layout.addWidget(self.processor)

        self.layout.addWidget(QLabel("Memóriaigény (MB)"))
        self.memory = QLineEdit(self)
        self.memory.setValidator(QIntValidator())
        self.layout.addWidget(self.memory)

        self.update_list()

        self.save_button = QPushButton("Mentés")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save)

    def update_list(self):
        self.program_count.clear()
        self.memory.clear()
        self.processor.clear()
        cluster = State().read_from_path(self.cluster_path)
        self.program_list.currentIndexChanged.disconnect()
        self.program_list.clear()
        self.program_list.addItem("", None)
        for key, i in enumerate(cluster.cluster_processes):
            self.program_list.addItem(i.name, key)
        self.program_list.currentIndexChanged.connect(self.set_values)

    def set_values(self, index):
        cluster = State().read_from_path(self.cluster_path)
        if index:
            index -= 1
            process = cluster.cluster_processes[index]
            self.program_count.setText(str(process.count))
            self.processor.setText(str(process.processor))
            self.memory.setText(str(process.memory))
        else:
            self.program_count.clear()
            self.processor.clear()
            self.memory.clear()

    def save(self):
        if not self.program_list.currentText():
            QMessageBox.warning(
                self,
                "Hiba",
                "Nincs semmi kiválasztva",
            )
            return

        cluster = State().read_from_path(self.cluster_path)
        current = self.program_list.currentIndex() - 1
        cluster.cluster_processes[current].count = int(self.program_count.text())
        cluster.cluster_processes[current].processor = int(self.processor.text())
        cluster.cluster_processes[current].memory = int(self.memory.text())
        cluster.write_to_path(self.cluster_path)

        QMessageBox.information(
            self,
            "Mentve",
            "Sikeresen elmentve"
        )
        self.update_list()


class RunProgram(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path
        cluster = State().read_from_path(cluster_path)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Program futtattása</h1>"))

        self.layout.addWidget(QLabel("Számítógép neve"))
        self.computer_list = QComboBox()
        self.layout.addWidget(self.computer_list)

        self.layout.addWidget(QLabel("Program neve"))
        self.program_list = QComboBox()
        self.layout.addWidget(self.program_list)
        self.program_list.currentIndexChanged.connect(self.set_value)

        self.layout.addWidget(QLabel("Egyedi azonosító"))
        self.unique_id = QLabel()
        self.layout.addWidget(self.unique_id)

        self.layout.addWidget(QLabel("Létrehozva"))
        self.created_at = QLabel()
        self.layout.addWidget(self.created_at)

        self.layout.addWidget(QLabel("Max processzor használat"))
        self.processor_usage = QLabel()
        self.layout.addWidget(self.processor_usage)

        self.layout.addWidget(QLabel("Max memória használat"))
        self.memory_usage = QLabel()
        self.layout.addWidget(self.memory_usage)

        self.memory = 0
        self.processor = 0

        self.update_list()

        self.save_button = QPushButton("Indítás")
        self.layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save)

    def update_list(self):
        cluster = State().read_from_path(self.cluster_path)
        self.computer_list.clear()
        computer_options = [i.name for i in cluster.computers]
        self.computer_list.addItem("", None)
        for key, i in enumerate(computer_options):
            self.computer_list.addItem(i, key)

        self.program_list.currentIndexChanged.disconnect()
        self.program_list.clear()
        self.program_list.addItem("", None)
        for key, i in enumerate(cluster.cluster_processes):
            self.program_list.addItem(i.name, key)
        self.program_list.currentIndexChanged.connect(self.set_value)

    def set_value(self, index):
        if index:
            index -= 1
            cluster = State().read_from_path(self.cluster_path)
            process = cluster.cluster_processes[index]
            uid = ""
            while uid == "":
                for i in range(6):
                    uid += random.choice(string.ascii_lowercase)
                uids = []
                for i in cluster.computers:
                    for x in i.processes:
                        uids.append(x.uid)
                if uid in uids:
                    uid = ""
            self.unique_id.setText(uid)
            self.created_at.setText(str(datetime.datetime.strftime(datetime.datetime.now(), "%Y.%m.%d %H:%M")))
            self.processor_usage.setText(f"{process.processor} millimag")
            self.memory_usage.setText(f"{process.memory} MB")

            self.memory = process.memory
            self.processor = process.processor
        else:
            self.unique_id.clear()
            self.created_at.clear()
            self.processor_usage.clear()
            self.memory_usage.clear()

            self.memory = 0
            self.processor = 0

    def save(self):
        if not self.computer_list.currentText() or not self.program_list.currentText():
            QMessageBox.warning(
                self,
                "Hiba",
                "Nincs számítógép vagy program kiválasztva"
            )
            return
        current = self.computer_list.currentIndex() - 1

        cluster = State().read_from_path(self.cluster_path)
        computer_data = cluster.computers[current]
        if sum(x.memory_usage for x in computer_data.processes) + self.memory > computer_data.memory_capacity:
            QMessageBox.critical(
                self,
                "Hiba",
                "Nincs elég memória kapacitás"
            )
            return
        if sum(x.processor_usage for x in computer_data.processes) + self.processor > computer_data.processor_capacity:
            QMessageBox.critical(
                self,
                "Hiba",
                "Nincs elég proszesszor kapacitás"
            )
            return

        computer_data.processes.append(
            ProcessState(
                name=self.program_list.currentText(),
                uid=self.unique_id.text(),
                started_at=datetime.datetime.fromisoformat(self.created_at.text().replace(" ", "T").replace(".", "-")),
                memory_usage=self.memory,
                processor_usage=self.processor,
                active=True
            )
        )
        cluster.write_to_path(self.cluster_path)

        QMessageBox.information(
            self,
            "Mentve",
            "Folyamat sikeresen elindítva"
        )

        self.update_list()


class StopProcess(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Folyamat leállítása</h1>"))
        self.computer_list = QComboBox()
        self.layout.addWidget(self.computer_list)
        self.computer_list.currentIndexChanged.connect(self.set_value)

        self.layout.addWidget(QLabel("Folyamat neve"))
        self.process_list = QListWidget()
        self.layout.addWidget(self.process_list)
        self.process_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        self.update_list()
        self.stop_button = QPushButton("Leállítás")
        self.layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop)

    def update_list(self):
        self.computer_list.currentIndexChanged.disconnect()
        cluster = State().read_from_path(self.cluster_path)
        self.computer_list.clear()
        computer_options = [i.name for i in cluster.computers]
        self.computer_list.addItem("", None)
        for key, i in enumerate(computer_options):
            self.computer_list.addItem(i, key)
        self.process_list.clear()
        self.computer_list.currentIndexChanged.connect(self.set_value)

    def set_value(self, index):
        if index != 0:
            self.process_list.clear()
            index -= 1
            cluster = State().read_from_path(self.cluster_path)
            current_computer_processes = [i.processes for i in cluster.computers if i.name == self.computer_list.currentText()]
            if len(current_computer_processes[0]) == 0:
                return
            processes = current_computer_processes[0]
            self.process_list.clear()
            for i in processes:
                self.process_list.addItem(f"{i.name} - {i.uid}")
        else:
            self.process_list.clear()

    def stop(self):
        messages = []
        cluster = State().read_from_path(self.cluster_path)
        for i in self.process_list.selectedItems():
            name = i.text().split(" - ")[0]
            uid = i.text().split(" - ")[1]
            chosen_computer = [y for y in cluster.computers if y.name == self.computer_list.currentText()][0]
            chosen_program = [x for x in chosen_computer.processes if x.name == name and x.uid == uid][0]
            chosen_computer.processes.remove(chosen_program)
            cluster.write_to_path(self.cluster_path)
            messages.append(f"{chosen_program.name} sikeresen leállítva!")

        QMessageBox.information(
            self,
            "Sikeres művelet",
            "\n".join(messages),
        )
        self.update_list()


class SearchProcess(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Folyamat keresése</h1>"))
        self.process_list = QLineEdit()
        self.process_list.setPlaceholderText("Keresés")
        self.process_list.textEdited.connect(self.search)
        self.process_list.setClearButtonEnabled(True)
        self.layout.addWidget(self.process_list)

        self.result_window = QWidget()
        self.result_window.setLayout(QVBoxLayout())
        self.layout.addWidget(self.result_window)

    def update_list(self):
        self.search("")
        self.process_list.setFocus()

    def search(self, text):
        # Clear the result window
        # Store the widget as an instance attribute
        layout = self.result_window.layout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        # Scroll area setup
        scroll_area = QScrollArea()
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)

        # Read cluster data
        cluster = State().read_from_path(self.cluster_path)
        for computer in cluster.computers:
            for process in computer.processes:
                if process.name.startswith(text):
                    content_layout.addWidget(QLabel(f"<h3>{process.name}</h3>"))
                    content_layout.addWidget(QLabel(f"Azonosító: {process.uid}"))
                    content_layout.addWidget(QLabel(f"Memória igény: {process.memory_usage} MB"))
                    content_layout.addWidget(QLabel(f"Processzor igény: {process.processor_usage} millimag"))
                    content_layout.addWidget(QLabel(f"Státusz: {'Aktív' if process.active else 'Inaktív'}"))
                    content_layout.addWidget(QLabel(f"Elindítva: {process.started_at.isoformat(' ').split('T')[0].replace('-', '. ')}"))
                    content_layout.addWidget(QLabel(f"Számítógép: {computer.name}"))
                    content_layout.addWidget(QLabel("<hr>"))
        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Final widget display settings


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(QPalette(QColor("#2b2d30")))
    window = SearchProcess()
    window.show()
    app.exec()
