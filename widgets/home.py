import ctypes
import os
import sys

from PySide6.QtGui import Qt, QPalette, QColor, QIntValidator
from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QComboBox, QLabel, \
    QStyleFactory, QFrame, QLineEdit, QMessageBox

from modules.models import State, Computer

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


class Home(QFrame):
    def __init__(self, cluster_path="../cluster0"):
        super().__init__()
        self.cluster_path = cluster_path

        self.cluster_path = cluster_path
        self.cluster = State().read_from_path(cluster_path)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setFixedWidth(300 * scaleFactor)

        self.layout.addWidget(QLabel("<h1>Főoldal</h1>"))

        self.label = QLabel()
        self.layout.addWidget(self.label)

    def update_list(self):
        osszes = State().read_from_path(self.cluster_path)

        programok = {}
        prog_szam_active = {}
        prog_szam_inactive = {}

        no_hiba = True

        errors = []

        for i in osszes.cluster_processes:
            programok[i.name] = i.count
            prog_szam_active[i.name] = 0
            prog_szam_inactive[i.name] = 0

        for f in osszes.computers:
            processor = f.processor_capacity
            memory = f.memory_capacity

            ossz_proc = 0
            ossz_memo = 0

            for k in f.processes:
                if k.active:
                    prog_szam_active[k.name] += 1
                else:
                    prog_szam_inactive[k.name] += 1

                ossz_proc += k.processor_usage
                ossz_memo += k.memory_usage

            if ossz_proc > processor:
                errors.append(
                    f"Nagyobb a programok processzor igénye a {f.name} gépen!\n\tMaximális kapacitás:{processor}\n\tKért kapacitás: {ossz_proc}")
                no_hiba = False
            if ossz_memo > memory:
                errors.append(
                    f"Nagyobb a programok memória igénye a {f.name} gépen!\n\tMaximális kapacitás:{memory}\n\tKért kapacitás: {ossz_memo}")
                no_hiba = False

        for i in programok:

            if prog_szam_active[i] < programok[i]:
                errors.append(
                    f"Kevesebb aktív program van a {i} programból!\n\tKívánt Aktív: {programok[i]}\n\tAktív: {prog_szam_active[i]}\n\tInaktív: {prog_szam_inactive[i]}")
                no_hiba = False
            if prog_szam_active[i] + prog_szam_inactive[i] > programok[i]:
                errors.append(
                    f"Több program fut a {i} programból!\n\tKívánt szám: {programok[i]}\n\tAktív:{prog_szam_active[i]}\n\tInaktív:{prog_szam_inactive[i]}")
                no_hiba = False
        self.label.setText("\n".join(errors))
        if no_hiba:
            self.label.setText("Nincsen Hiba")
