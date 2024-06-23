#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import QPointF, Qt

from dst.visual.phasors.PhasorPlotter import PhasorPlotter
from dst.math.fourier_series import square_wave, Phasor


class PhasorProjection1D(QWidget):
    G_SCALER = 70

    WAVE_MAX_LENGTH = 1000  # Maksimaalne arv lõppsignaali punkte, mida kuvame
    Y_POS_INCREMENT = 0.25  # y-telje nihutamise samm #0.25
    Y_POS_OFFSET = 500   # Lõppsignaali kaugus faasoritest y-teljel

    DELTA_TIME = 0.05    # Diskreetimise samm
    nr_of_terms = 1      # Mitu sageduskomponenti välja arvutame
    current_time = 0     # Praegune ajahetk

    path = []


    def __init__(self):
        super().__init__()
        self.phasor_plotter = PhasorPlotter(self)


    def update(self):
        """
        Meetod, mis uuendab programmi seisu suurendades hetke aega ja luues vastavalt sellele kuvatava väljundi.
        """
        self.phasor_plotter.phasors.clear()
        self.current_time += self.DELTA_TIME  # Liigutame aega edasi

        # 2.2 Ülesanne
        # Sisesta järjendisse self.phasor_plotter.phasors üks Phasor tüüpi faasor sagedusega 1, magnituudiga 1 ja faasiga 0
        # TODO
        #self.phasor_plotter.phasors.append(Phasor(1, 1, 0))

        # 3.2 Ülesanne
        # Kommenteeri välja 2.2 ülesandes tehtud faasori lisamine.
        # Arvuta nr_of_terms arv faasoreid ja lisa järjendisse self.phasor_plotter.phasors
        # TODO
    	
        # Arvutame faasorid ja lisame need plotteri faasorite järjendisse
        for term in range(0, self.nr_of_terms):
            self.phasor_plotter.phasors.append(square_wave(term))

        #arvutame iga faasori positsiooni vastavalt sagedusele,magnituudile ja faasile 
        self.phasor_plotter.calculatePhasorCircles(self.current_time)

        # 3.5 Ülesanne
        # Lisa välja arvutatud punkt väljundisse (kasutades add_point() meetodit)
        # y-koordinaadi väärtuseks võib esialgu panna 0. Ära unusta seda 3.7 ülesandes muutmast.
        # TODO
        self.add_point([self.phasor_plotter.x_pos, self.Y_POS_OFFSET])
        super().update()  # Trigger paintEvent


    # Meetod kutsutakse välja super().update() meetodi poolt uue seisu joonistamiseks graafikule
    def paintEvent(self, event):
        """
        Meetod, mis joonistab faasorid ja nende põhjal arvutatud signaali.
        """
        qp = QPainter()
        qp.begin(self)
        qp.setBackgroundMode(Qt.BGMode.OpaqueMode)
        # Joonistab faasorid
        self.phasor_plotter.paint(qp)

        # Muudab graafiku pliiatsi värvi signaali joonistamiseks.
        qp.setPen(QPen(QColor.fromRgb(51, 153, 136), 3))

        # Joonistab kogu seni arvutatud signaali
        self.drawPath(qp)

        # 3.8 Ülesanne
        # Joonistage joon faasorite summa tipust nihutatud lõppsignaalini
        # TODO
        qp.drawLine(QPointF(self.phasor_plotter.x_pos, self.phasor_plotter.y_pos), QPointF(self.phasor_plotter.x_pos, self.Y_POS_OFFSET))

        qp.end()


    def keyPressEvent(self, event):
        """
        Meetod, milles loetakse klaviatuurilt nooleklahvi sisendeid ▲ või ▼
        ja vastavalt sellele suurendatakse või vähendatakse muutujat nr_of_terms.
        """
        key = event.key()
        if key == Qt.Key_Up:
            self.nr_of_terms += 1
        elif key == Qt.Key_Down and self.nr_of_terms > 0:
            self.nr_of_terms -= 1


    def add_point(self, new_point):
        """
        Meetod, mis lisab antud punkti lõppsignaalile

        Sisendid:
        new_point - lisatav punkt (x, y) koordinaatide paarina
        """
        qpoint = QPointF(new_point[0], new_point[1])
        self.path = [QPointF(point.x(), point.y() + self.Y_POS_INCREMENT) for point in self.path]
        self.path.insert(0, qpoint)
        self.path = self.path[:self.WAVE_MAX_LENGTH]


    def drawPath(self, qp):
        """
        Meetod, mis joonistab jooned seni arvutatud lõppsignaali punktide vahele

        Sisendid:
        qp - QPainter klassi isend joonistamiseks
        """
        for i, point in enumerate(self.path):
            if i != len(self.path) - 1:
                qp.drawLine(point, self.path[i + 1])
