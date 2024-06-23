#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget
from PyQt5.QtMultimedia import QSound
from scipy.io import wavfile
import tempfile
import os
import numpy as np

class AudioPlayer(QWidget):
    def __init__(self, grid, row, task, sr, parent=None):
        super().__init__(parent=parent)
        self.task = task
        self.sr = sr
        self.original_play_button = QPushButton("Esita originaalfail")
        self.filtered_play_button = QPushButton("Esita filtreeritud heli")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.original_play_button)
        self.button_layout.addWidget(self.filtered_play_button)
        self.original_play_button.clicked.connect(self.play_original)
        self.filtered_play_button.clicked.connect(self.play_filtered)
        self.original_playing = False
        self.filtered_playing = False
        self.qs = None
        self.sound_temp_file = tempfile.NamedTemporaryFile('w', delete=False)
        self.temp_file_name = self.sound_temp_file.name
        self.sound_temp_file.close()
        grid.addLayout(self.button_layout, row, 0, 1, 3)


    def play_original(self):
        if self.original_playing: # peatamine
            self.original_play_button.setText("Esita originaalfail")
            self.original_playing = False
            self.qs.stop()
        else: # käivitamine
            wavfile.write(self.temp_file_name, self.sr, (self.task.get_unfiltered_data() * 32767).astype(np.int16))
            if self.qs:
                self.qs.stop()
                del self.qs
            self.qs = QSound(self.temp_file_name)
            self.qs.setLoops(QSound.Infinite)
            self.qs.play()
            self.original_play_button.setText("Peata originaali esitus")
            self.filtered_play_button.setText("Esita filtreeritud heli")
            self.filtered_playing = False
            self.original_playing = True

    def play_filtered(self):
        if self.filtered_playing: # peatamine
            self.filtered_play_button.setText("Esita filtreeritud heli")
            self.filtered_playing = False
            self.qs.stop()
        else: # käivitamine
            wavfile.write(self.temp_file_name, self.sr, (self.task.get_filtered_data() * 32767).astype(np.int16))
            if self.qs:
                self.qs.stop()
                del self.qs
            self.qs = QSound(self.temp_file_name)
            self.qs.setLoops(QSound.Infinite)
            self.qs.play()
            self.filtered_play_button.setText("Peata filtreeritud heli esitus")
            self.original_play_button.setText("Esita originaalfail")
            self.original_playing = False
            self.filtered_playing = True


class controlPanel(QWidget):
    def __init__(self, grid, row, task, parent=None):
        super().__init__(parent=parent)
        self.filtered_play_button = QPushButton("Kuva aegruumi esitus")
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.original_play_button)
        self.button_layout.addWidget(self.filtered_play_button)
        self.original_play_button.clicked.connect(self.play_original)
        self.filtered_play_button.clicked.connect(self.play_filtered)
        self.original_playing = False
        self.filtered_playing = False
        self.qs = None
        grid.addLayout(self.button_layout, row, 0, 1, 3)
