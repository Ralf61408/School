#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys, math
import os
from pyqtgraph.Qt import QtCore, QtWidgets
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from dst.visual.phasors.PhasorProjection1D import PhasorProjection1D
from dst.visual.phasors.PhasorProjection2D import PhasorProjection2D
from dst.visual.phasors.PhasorUserInterface import PhasorUserInterface

from dst.math.fourier_series import create_8like_signal
from dst.fourier.dft import dft, idft, magnituudid_faasid
from andmed.varia.p05_sample_signals import signal1, signal2, signal3, signal4, test8_signal1, test8_signal2
from abi.visual.plot_stem import plot_stem


def yl1():
    t = np.arange(0, len(signal1), 1)
    pendulum1 = signal1

    # Loome graafikud kasutades PyQtGraph'i
    win = pg.GraphicsLayoutWidget(show=True, title="Fourier' teisendus")
    p1 = win.addPlot(x=t, y=pendulum1, title="Signaal ajas")
    p1.addLegend()
    p1.setLabel('left', "Väärtus", units='y')
    p1.setLabel('bottom', "Ajahetk", units='n')
    p1.showGrid(x=True, y=True)
    win.nextRow()
    
    dft_minu = dft(signal1)
    avaldis_magnituudid, avaldis_faasid = magnituudid_faasid(dft_minu)
    p2 = win.addPlot(title = "Implementeeritud Fourier' teisenduse tulemus")
    plot_stem(p2, avaldis_magnituudid, avaldis_faasid)
    p2.addLegend()
    p2.setLabel('left', "magnituud")
    p2.setLabel('bottom', "sagedus", units='n')
    p2.showGrid(x=True, y=True)
    win.nextRow()


    p3 = win.addPlot(title = "Numpy Fourier' teisenduse tulemus")
    npdft = np.fft.fft(signal1)
    numpy_dft2 = np.absolute(npdft)
    numpy_faas = np.angle(npdft)
    plot_stem(p3, numpy_dft2, numpy_faas)
    p3.addLegend()
    p3.setLabel('left', "magnituud")
    p3.setLabel('bottom', "sagedus", units='n')
    p3.showGrid(x=True, y=True)
    win.nextRow()
    

    teisendatud_dft = idft(npdft)
    t2 = np.arange(0, len(teisendatud_dft), 1)
    a = np.array(teisendatud_dft)

    p4 = win.addPlot(x=t2, y=a, pen=(0, 255, 0), title = "Signaal ajas uuesti")
    p4.addLegend()
    p4.setLabel('left', "Väärtus", units='y')
    p4.setLabel('bottom', "Ajahetk", units='n')
    p4.showGrid(x=True, y=True)

    QtWidgets.QApplication.instance().exec_()
    pass


def yl2_3():
    app = QApplication(sys.argv)

    SCRIPT_PATH = os.path.dirname(__file__)
    with open(os.path.join(SCRIPT_PATH, "abi/visual/styles.qss")) as file:
        app.setStyleSheet(file.read())

    projector = PhasorProjection1D()
    userInterface = PhasorUserInterface(projector, 20)

    sys.exit(app.exec_())


def yl4():
    app = QApplication(sys.argv)

    SCRIPT_PATH = os.path.dirname(__file__)
    with open(os.path.join(SCRIPT_PATH, "abi/visual/styles.qss")) as file:
        app.setStyleSheet(file.read())

    signaali_testid()

    eight_signal1, eight_signal2 = create_8like_signal(800)
    projector = PhasorProjection2D(signal3, signal4)
    userInterface = PhasorUserInterface(projector, 20)

    sys.exit(app.exec_())


def signaali_testid():
    # Yl4 testsignaali õigsuse kontrollimine
    np.testing.assert_array_equal(np.round(np.array(test8_signal1), 5),
                                  np.round(np.array(create_8like_signal()[0]), 5))
    np.testing.assert_array_equal(np.round(np.array(test8_signal2), 5),
                                  np.round(np.array(create_8like_signal()[1]), 5))
    print("Testid edukalt läbitud")


def main():
    #yl1()
    #yl2_3()
    yl4()


if __name__ == "__main__":
    main()

