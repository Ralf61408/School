#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget

from dst.visual.phasors.PhasorPlotter import PhasorPlotter
from dst.fourier.dft import dft


class PhasorProjection2D(QWidget):
    WINDOW_WIDTH = 1080
    WINDOW_HEIGHT = 800
    G_SCALER = 1

    WAVE_MAX_LENGTH = 10000

    DELTA_TIME = 0    # Diskreetimise samm. See tuleb paika panna __init__ meetodis vastavalt juhendile
    current_time = 0  # Praegune ajahetk

    path = []


    def __init__(self, signal1, signal2):
        super().__init__()

        # 4.2 Ülesanne
        # Arvuta sisendsignaalidest signal1 ja signal2 DFT
        # TODO
        self.fourier_x = dft(signal1)
        self.fourier_y = dft(signal2)

        # jagan iga faasori magnituudi signaali pikkusega
        signal_x_length = len(signal1)  
        signal_y_length = len(signal2)

        for phasor in self.fourier_x:
            phasor.magnitude /= signal_x_length
        for phasor in self.fourier_y:
            phasor.magnitude /= signal_y_length
        

        self.fourier_x = sorted(self.fourier_x, key=lambda x: x.magnitude, reverse=True)
        self.fourier_y = sorted(self.fourier_y, key=lambda x: x.magnitude, reverse=True)

        # 4.4 Ülesanne
        # Initsialiseeri faasorite summeerijad ja sea korrektsed parameetrid
        # TODO
        self.DELTA_TIME = (2*np.pi)/len(self.fourier_y)

        self.x_phasor_plotter = PhasorPlotter(self)
        a = self.x_phasor_plotter
        a.phasors = self.fourier_x

        self.y_phasor_plotter = PhasorPlotter(self)
        b = self.y_phasor_plotter
        b.phasors = self.fourier_y

        self.x_phasor_plotter.X_ORIGIN = 540
        self.y_phasor_plotter.X_ORIGIN = 100

        self.x_phasor_plotter.Y_ORIGIN = 150
        self.y_phasor_plotter.Y_ORIGIN = 360

        self.y_phasor_plotter.ROTATION_OFFSET = -np.pi/2





    # Meetod kutsutakse välja QTimeri poolt uue seisu arvutamiseks
    def update(self):
        """
        Meetod, mis uuendab programmi seisu suurendades hetke aega ja vastavalt sellele kuvatavat väljundit.
        """
        self.x_phasor_plotter.calculatePhasorCircles(self.current_time)
        self.y_phasor_plotter.calculatePhasorCircles(self.current_time)

        # 4.7 Ülesanne
        # Kutsuge meetod self.add_point() õigete argumentidega
        # TODO
        self.add_point([self.x_phasor_plotter.x_pos, self.y_phasor_plotter.y_pos])
        self.current_time += self.DELTA_TIME
        super().update()


    # Meetod kutsutakse välja super().update() meetodi poolt uue seisu joonistamiseks graafikule
    def paintEvent(self, event):
        """
        Meetod, mis joonistab faasorid ja nende põhjal arvutatud signaali.
        """
        qp = QPainter()
        qp.begin(self)
        qp.setBackgroundMode(Qt.BGMode.OpaqueMode)
        self.x_phasor_plotter.paint(qp)  # Joonistab x-telje faasorid
        self.y_phasor_plotter.paint(qp)  # Joonistab y-telje faasorid

        # Muudab graafiku pliiatsi värvi signaali joonistamiseks.
        qp.setPen(QPen(QColor.fromRgb(51, 153, 136), 3))
        self.drawPath(qp) # Joonistab joone graafikule

        # Joonistan joone faasorite summa tipust (x_pos, y_pos) kuni lõpp-punktini (x_end, Y_POS_OFFSET)
        qp.drawLine(QPointF(self.x_phasor_plotter.x_pos, self.x_phasor_plotter.y_pos), QPointF(self.x_phasor_plotter.x_pos, self.y_phasor_plotter.y_pos))
        qp.drawLine(QPointF(self.y_phasor_plotter.x_pos, self.y_phasor_plotter.y_pos), QPointF(self.x_phasor_plotter.x_pos, self.y_phasor_plotter.y_pos))

        qp.end()


    def add_point(self, new_point):
        """
        Meetod, mis lisab antud punkti lõppsignaalile

        Sisendid:
        new_point - lisatav punkt (x, y) koordinaatide paarina
        """
        qpoint = QPointF(new_point[0], new_point[1])
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
