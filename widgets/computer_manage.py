import sys, os, ctypes

from PySide6.QtGui import Qt, QPalette, QColor, QDoubleValidator, QIntValidator
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, \
    QStyleFactory, QHBoxLayout, QFileDialog, QListWidget, QSpacerItem, QSizePolicy, QFrame, QLineEdit, QMessageBox, \
    QProgressBar

from modules.models import State, Computer

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class ComputerAdd(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path
        self.cluster = State().read_from_path(cluster_path)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("<h1>Hozzáadás</h1>"))

        self.pc_name = QLineEdit(self)

        self.layout.addWidget(QLabel("Számítógép neve"))
        self.layout.addWidget(self.pc_name)

        self.layout.addWidget(QLabel("Memória kapacitás"))

        self.memory = QLineEdit(self)
        self.memory.setValidator(QIntValidator())
        self.layout.addWidget(self.memory)

        self.layout.addWidget(QLabel("Processzot kapacitás"))

        self.processor = QLineEdit(self)
        self.processor.setValidator(QIntValidator())
        self.layout.addWidget(self.processor)

        self.submit = QPushButton("Mentés")
        self.submit.clicked.connect(self.save)
        self.layout.addWidget(self.submit)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.setFixedWidth(300 * scaleFactor)

    def save(self):
        self.cluster = State().read_from_path(self.cluster_path)
        if not self.pc_name.text() or not self.memory.text() or not self.processor.text() or not self.pc_name.text().isalnum():
            QMessageBox.critical(
                self,
                "Hiba",
                "Hibás érték(ek)"
            )
            return

        if os.path.exists(os.path.join(self.cluster_path, self.pc_name.text())):
            QMessageBox.warning(
                self,
                "Hiba",
                "Már létezik"
            )
            return

        self.cluster.computers.append(Computer(
            name=self.pc_name.text(),
            processor_capacity=self.processor.text(),
            memory_capacity=self.memory.text(),
        ))
        self.cluster.write_to_path(self.cluster_path)
        QMessageBox.information(
            self,
            "Mentve",
            "Sikeresen létrehozva"
        )
        self.pc_name.clear()
        self.memory.clear()
        self.processor.clear()


class ComputerRemove(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path
        self.cluster = State().read_from_path(cluster_path)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Törlés</h1>"))

        self.layout.addWidget(QLabel("Számítógép neve"))
        self.pc_name = QComboBox(self)
        self.update_list()
        self.layout.addWidget(self.pc_name)


        self.delete_button = QPushButton("Törlés")
        self.delete_button.clicked.connect(self.delete_computer)
        self.layout.addWidget(self.delete_button)

    def update_list(self):
        self.cluster = State().read_from_path(self.cluster_path)
        self.pc_name.clear()
        self.pc_name.addItem("", None)
        for key, i in enumerate(self.cluster.computers):
            self.pc_name.addItem(i.name, key)

    def delete_computer(self):
        if not self.pc_name.currentIndex():
            QMessageBox.critical(
                self,
                "Hiba",
                "Nincs kiválasztva semmi"
            )
            return
        lista = {}
        index = self.pc_name.itemData(self.pc_name.currentIndex())
        no_hiba = True
        for f in self.cluster.computers[index].processes:
            if f.active:
                no_hiba = False
            lista[f.name] = f"A {f.name} program aktiválva lett: {f.started_at}-kor\n\tStátusza: {"Aktív" if f.active else "Inaktív"}"
        if no_hiba:
            self.cluster.computers.pop(index)
            self.cluster.write_to_path(self.cluster_path)
            QMessageBox.information(
                self,
                "Mentve",
                "Sikeresen törölve"
            )
        else:
            QMessageBox.warning(
                self,
                "Nem lehet törölni mivel van futó program!",
                "\n".join(lista[h] for h in lista)
            )

        self.update_list()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    app.setPalette(QPalette(QColor("#2b2d30")))
    window = ComputerRemove()
    window.show()
    app.exec()
