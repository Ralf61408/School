#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt

class PhasorUserInterface(QWidget):
    WINDOW_WIDTH = 1080 # Soovitud akna mõõtmed
    WINDOW_HEIGHT = 800
    layout = QGridLayout() # Võimaldab kasutajaliidese elemente lisada ruudustiku koordinaatidele
    timer = QTimer() # Kasutame seisu jooksvaks uuendamiseks

    def __init__(self, projector, update_period):
        super().__init__()
        self.setLayout(self.layout)
        self.update_period = update_period
        self.projector = projector

        # Loome nupu animatsiooni peatamiseks/jätkamiseks
        self.pause_button = QPushButton("Peata / jätka")
        # Nupu vajutamisel kutsutakse välja siin määratud meetod
        self.pause_button.clicked.connect(self.toggle_timer)

        # Loome nupu ühe ajasammu teostamiseks
        self.single_button = QPushButton("Tee üks samm")
        self.single_button.clicked.connect(self.projector.update)

        # Paneme kõik kolm loodud kasutajaliidese elementi ritta indeksiga 0, järjestikustesse veergudesse
        self.layout.addWidget(self.pause_button, 0, 0)
        self.layout.addWidget(self.single_button, 0, 1)

        # Viimaks lisame kasutajaliidesesse objekti, kuhu saame teha joonistusi
        # See objekt on kogu kasutajaliidese laiune ja hõlmab seega mõlemat 2 veergu
        self.layout.addWidget(self.projector, 1, 0, 1, 2)

        # Alustame animatsiooni vastavalt soovitud uuendamise perioodile
        self.timer.timeout.connect(self.projector.update)
        self.timer.start(update_period)

        # Loome kasutajaliidese akna ja lubab selle kuvamise rakenduse käivitamisel
        self.setGeometry(300, 300, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle('Faasorid')

        # Teeme kindlaks, et klahvivajutuse sündmused jõuaksid joonistamise ala elemendile
        self.setFocusPolicy(Qt.NoFocus)
        self.pause_button.setFocusPolicy(Qt.NoFocus)
        self.single_button.setFocusPolicy(Qt.NoFocus)
        self.projector.setFocus()

        self.show()

    def toggle_timer(self):
        # Animatsiooni peatamiseks ja jätkamiseks vahetame QTimer'i olekut
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.update_period)
