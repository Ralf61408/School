#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QWidget
import numpy as np


class PhasorPlotter(QWidget):

    def __init__(self, parent, X_ORIGIN=500, Y_ORIGIN=150) -> None:
        super().__init__(parent=parent)
        self.G_SCALER = parent.G_SCALER
        self.X_ORIGIN = X_ORIGIN
        self.Y_ORIGIN = Y_ORIGIN

        # Need on x,y stardipositsioonid, kuhu hakatakse igal uuendamisel liitma
        #   sageduskomponentide avaldatavat x,y positsioonide nihet.
        self.x_pos = X_ORIGIN
        self.y_pos = Y_ORIGIN

        self.ROTATION_OFFSET = 0  # Faasinihe kõikidele sageduskomponentidele
        self.phasors = []  # Järjend faasoritest, mille elemendid on Phasor klassi isendid
        self.circles = []  # Järjend faasorite ringidest, mille elemendid on Circle klassi isendid


    def paint(self, qp):
        """
        Meetod, mis joonistab faasorid antud ajahetkel.

        Sisendid:
        qp: QPainter objekt, millega saab joonistada

        Vaadake https://doc.qt.io/qt-5/qpainter.html#drawEllipse-3
          ja  https://doc.qt.io/qt-5/qpainter.html#drawLine-4
        """
        # Joonistab algpunkti
        qp.setPen(QPen(Qt.yellow, 3))
        qp.drawEllipse(QPointF(self.X_ORIGIN, self.Y_ORIGIN), 4, 4)
        qp.setPen(QPen(Qt.white, 2))
        # Ülesanne 2.2:
        # Joonistage ühe faasori ring ja vektor
        # Kasutage selleks self.circles järjendis olevat ringi ning self.x_pos ja self.y_pos väärtusi.
        #if self.circles:
            #võtame esimese ringi
           # circle = self.circles[0]
        
           # qp.drawEllipse(QPointF(circle.x, circle.y), circle.r, circle.r)

           # qp.drawLine(QPointF(circle.x, circle.y), QPointF(self.x_pos, self.y_pos))
       # else:
          #  print("tühi list")


        # Ülesanne 3.4:
        # Muutke ülesandes 2.2 loodud koodi nii, et joonistataks
        # iga faasori ring ja vektor järjendist self.circles.
        # TODO

        if self.circles:
        # Käime kõik ringid läbi
            for i in range(len(self.circles)):
                # Praegune ring
                circle = self.circles[i]

                # Joonistan praegusee ringi
                qp.drawEllipse(QPointF(circle.x, circle.y), circle.r, circle.r)

                # Kui see pole viimane ring, joonistan joone praegusest ringist järgmise ringi keskpunktini
                if i < len(self.circles) - 1:
                    next_circle = self.circles[i + 1]
                    qp.drawLine(QPointF(circle.x, circle.y), QPointF(next_circle.x, next_circle.y))
                else:
                    # Kui see on viimane ring, joonistan joone viimase ringi keskpunktist punktini (self.x_pos, self.y_pos)
                    qp.drawLine(QPointF(circle.x, circle.y), QPointF(self.x_pos, self.y_pos))
        else:
            print("tühi list")
                



    def calculatePhasorCircles(self, current_time):
        """
        Meetod, mis arvutab välja faasorite väärtused antud ajahetkel (current_time) ja summeerib nende mõju.
        Meetod salvestab kõikide faasorite ringid järjendisse self.circles
        ning lõpppunkti muutujatesse self.x_pos ja self.y_pos

        Sisendid:
        current_time - ajahetk, mille jaoks faasorite väärtused arvutatakse

        """
        self.x_pos = self.X_ORIGIN
        self.y_pos = self.Y_ORIGIN
        self.circles.clear()
        # Ülesanne 2.2:
        # Võta järjendist self.phasors esimene element, ning salvesta ringi keskpunkt
        # ja raadius järjendisse self.circles kasutades Circle klassi
        # Faasori otspunkt salvesta muutujatesse self.x_pos ja self.y_pos
        # Korruta eelnevalt ka G_SCALERiga läbi, et faasor visuaalselt suurem paistaks

        #muutuja = self.phasors[0]
        ##self.circles.append([[self.x_pos, self.y_pos], self.G_SCALER * muutuja.magnitude]) see pole hea
        #self.circles.append(Circle(self.x_pos, self.y_pos, self.G_SCALER * muutuja.magnitude))
        #self.x_pos += self.G_SCALER *  (muutuja.magnitude * np.cos(current_time * muutuja.frequency + muutuja.phase))
        #self.y_pos -= self.G_SCALER *  (muutuja.magnitude * np.sin(current_time * muutuja.frequency + muutuja.phase))


        # Ülesanne 3.3:
        # Täienda 2.2 ülesandes tehtud koodi.
        # Käi läbi iga faasor ja arvuta selle mõju algpositsioonile
        # Salvesta lõplikud koordinaadid väljadesse self.x_pos ja self.y_pos (korruta enne G_SCALER-iga läbi)
        # Salvesta self.circles järjendisse kõikide faasorite keskpunktide koordinaadid ja raadiused kasutades Circle klassi
        # TODO

      
        i = 0
        while i < len(self.phasors):
            muutuja = self.phasors[i]
            i = i + 1
            self.circles.append(Circle(self.x_pos, self.y_pos, self.G_SCALER * muutuja.magnitude))
            self.x_pos += self.G_SCALER *  (muutuja.magnitude * np.cos(current_time * muutuja.frequency+muutuja.phase+self.ROTATION_OFFSET))
            self.y_pos -= self.G_SCALER *  (muutuja.magnitude * np.sin(current_time * muutuja.frequency+muutuja.phase+self.ROTATION_OFFSET))


class Circle:

    def __init__(self, x, y, r):
        self.x = x  # Faasori ringi keskpunkti x koordinaat
        self.y = y  # Faasori ringi keskpunkti y koordinaat
        self.r = r  # Faasori ringi raadius


    # __repr__ meetod Python'is annab võimaluse valida, millist informatsiooni me soovime
    # näha, kui me prindime objekti käsureale või kasutame silurit.
    def __repr__(self):
        return f"Circle {{ midpoint: ({self.x}, {self.y}), radius: {self.r} }}"
