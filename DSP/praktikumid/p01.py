#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
from dst.device.read_from_arduino import read_data_from_serial
import math, serial, time
from PyQt5.QtWidgets import QApplication  # Use PyQt5.QtWidgets or PyQt6.QtWidgets
from PyQt5.QtGui import QFont  # Use PyQt5.QtGui or PyQt6.QtGui
import sys
##from PyQt5.QtGui import QFontDatabase



def yl2_1(N): #Summa märgi üleval või muutuja mida me soovime tuua 

    tulemus = 0 # Algväärtus tulemus 0

    for n in range(1, N + 1): # Loop, mis käib läbi arvude 1-st kuni x-ni (kaasaarvatud). 1 - n = 1 / Suur sigma 
        a = 1/n**n # Arvutame 1/n^n
        tulemus +=a # Lisame 1/n^n väärtuse tulemusele juurde

    return tulemus


def yl2_2(n, a):

    tulemus = 0
    vahetulemus1 = 0
    vahetulemus2 = 0
    
    for x in range(0, n + 1): # Loop, mis käib läbi arvude 0-st kuni x-ni (kaasaarvatud)
        vahetulemus1 = (4*math.sin(x)) # Arvutame 4 * sin(n)
        vahetulemus2 = vahetulemus1/(a*math.pi) # Jagame vahetulemus1 (a * pi)-ga
        tulemus +=vahetulemus2 # Lisame vahetulemus2 tulemusele juurde
        
    return tulemus


def yl2_3(M):

    tulemus = 0
    vahetulemus = 0

    for x in range(0, M + 1):
        vahetulemus = (math.cos(x) - (1j * math.sin(x)))
        tulemus += vahetulemus

    return tulemus


def yl2_4(B, M, u):

    arv1 = 30
    tulemus = 0

    for x in range(1, arv1 + 1):  # Tsükkel, mis käib läbi arvude 1-st kuni 30-ni (kaasaarvatud)

        for b in range(u, B + 1): # Tsükkel, mis käib läbi arvude u-st kuni B-ni (kaasaarvatud)

            for m in range(4, M + 1): # Tsükkel, mis käib läbi arvude 4-st kuni M-ni (kaasaarvatud)

                korrutis_tehe = m * x
                euler_tehe = (math.e)**b
                vahetulemus = korrutis_tehe + euler_tehe
                tulemus += vahetulemus
    

    return tulemus


def yl2_5(A, k): # Suur np.pi avaldiste korrutamine

    tulemus = 1

    for a in range(1, A + 1):

        vahetulemus = (k*a + 1)/(3*k + a)
        tulemus *= vahetulemus

    return tulemus


def yl2_6(C, D, k, l):
     
    jagatis_tehe = 0
    tulemus = 1

    for c in range(k, C + 1):

        vahetulemus = 0

        for d in range(l, D + 1):
            jagatis_tehe = c / d
            vahetulemus += jagatis_tehe
        tulemus *= vahetulemus
        


    return tulemus


def yl2_7(f):
    
    n = 0
    avaldis = 0
    tulemus = 0
    N = len(f)

    for n in range(0, N):
        avaldis = ((f[n]) * math.cos(2*np.pi*0.75*(n - N)))/(n - N)
        tulemus += avaldis
    return tulemus


def yl2_8(a, f):
    
    avaldis_funktsioon = 0
    vahetulemus = 0
    N = len(f)

    for n in range(1, N):
        avaldis_funktsioon = (f[n-1]) + (f[n])
        vahetulemus += avaldis_funktsioon
    
    tulemus = a * vahetulemus
    return tulemus


def yl2_9(f, g):

    N = len(f) # Arvutame f pikkuse ja määrame selle N-iks
    M = len(g) # Arvutame g pikkuse ja määrame selle M-iks

    sum1=0
    for n in range(0, N): # Tsükkel, mis käib läbi kõik f elemendid
        sum1+=f[n]

    sum2=0
    for m in range(0, M):
        sum2+= g[m]

    return ((1/N)*sum1)*((1/M)*sum2)


def yl2():
    print(f"Yl1_1: {yl2_1(2)}")
    print(f"Yl1_2: {yl2_2(3, 2)}")
    print(f"Yl1_3: {yl2_3(10)}")
    print(f"Yl1_4: {yl2_4(3, 4, 2)}")
    print(f"Yl1_5: {yl2_5(1, 2)}")
    print(f"Yl1_6: {yl2_6(3, 2, 2, 1)}")
    print(f"Yl1_7: {yl2_7([1, 2, 3, 4, -5])}")
    print(f"Yl1_8: {yl2_8(2, [1, 2, 3])}")
    print(f"Yl1_9: {yl2_9([1, 2], [1, 2, 3])}")


def yl3_looped_sum(A):

    tulemus = 0

    for a in range(1, A + 1):

        vahetulemus = 4*a
        tulemus +=vahetulemus

    return tulemus


def yl3_vectorised_sum(A):
    
    array = np.arange(A+1)
    arvutus = 4 * array
    tulemus = arvutus.sum()

    return tulemus


def yl3_filtering_with_masks():

    maatriks = np.random.randint(201, size=(4,7))
    print(maatriks)
    a = np.mean(maatriks, axis=0) # igas veerus, kui axis=1, siis igas reas
    b = np.mean(maatriks)
    print("a", a)
    print("b", b)
    # Loome maski, kus iga veeru keskmine on suurem kui kogu maatriksi keskmine
    mask = a > b

    print (mask)
    # Filtreerime maatriksit maski abil, valides veerud, kus mask on True
    print(maatriks[:,mask])
    # maatriks[:, :]: Esimene : tähendab "vali kõik read", teine : tähendab "vali kõik veerud". 


def yl3():
    looped_times = []
    vectorised_times = []
    input_values = [1, 10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20240, 30240, 40240]
    trials = 1000
 
    for A in input_values:
        # implementeeritud valemi naiivse kuju töökiirus 
        looped_time_trials = []
        for _ in range(trials):
            start_time = time.perf_counter()
            yl3_looped_sum(int(A))
            looped_time_trials.append(time.perf_counter() - start_time) 
        average_looped_time = np.mean(looped_time_trials) * 1000
        looped_times.append(average_looped_time)
        print("looped times: ", looped_times)

        # implementeeritud valemi vektoriseeritud kuju töökiirus
        vectorised_time_trials = []
        for _ in range(trials):
            start_time = time.perf_counter()
            yl3_vectorised_sum(A)
            vectorised_time_trials.append(time.perf_counter() - start_time)
        average_vectorised_time = np.mean(vectorised_time_trials) * 1000
        vectorised_times.append(average_vectorised_time)
        print("vektor times: ", vectorised_times)

    ##average_looped_time = np.mean(looped_times) / 1000 # konverdime tagasi millisekunditeks
    ##average_vectorised_time = np.mean(vectorised_times) / 1000 # konverdime tagasi millisekunditeks

    ##print(f"Average looped sum time: {average_looped_time} milliseconds")
    ##print(f"Average vectorised sum time: {average_vectorised_time} milliseconds")

    
     # Plottimise osa
    # Initsaliseerime Qt rakendust
    app = QApplication(sys.argv)

    # Muudan kogu rakenduse teksti suurust
    font = QFont()
    font.setPointSize(20)  # Teen teksti suuremaks
    app.setFont(font)

    window = pg.GraphicsLayoutWidget(show=True, title="1000 katse implementeeritud valemi naiivse/vektoriseeritud kuju keskmine aeg millisekundites")
    plot = window.addPlot(title="<span style='font-size: 20pt;'>1000 katse implementeeritud valemi naiivse/vektoriseeritud kuju keskmine aeg millisekundites")
    plot.setLabels(left='Aeg (ms)', bottom='Massiivide pikkused')
    plot.addLegend()

    plot.plot(input_values, looped_times, pen='r', name="<span style='font-size: 20pt;'>1000 katse implementeeritud valemi naiivse kuju keskmine aeg millisekundites")
    plot.plot(input_values, vectorised_times, pen='b', name="<span style='font-size: 20pt;'>1000 katse implementeeritud valemi vektoriseeritud kuju keskmine aeg millisekundites")

    QApplication.exec_() 

# Signaalidega töötamisel on sageli graafikute x-teljel aeg või sagedus; y-teljel temperatuur, pinge, asukoht või võimendus.

def yl4():
    ##import pyqtgraph.examples
    # Loome NumPy't kasutades aja väärtuste massiivi,
    # kus väärtused on 0st 12ni, 0.03 ühikulise sammuga (kokku 400 väärtust)

    # Initsaliseerime Qt rakendust
    app = QApplication(sys.argv)

    # Muudan kogu rakenduse teksti suurust
    font = QFont()
    font.setPointSize(20)  # Teen teksti suuremaks
    app.setFont(font)

    t = np.arange(0, 24, 0.03)
    pendulum1 = 5 * np.cos(t)
    pendulum2 = 5 * np.sin(t - np.pi/2)
    # pyqtgraph.examples.run()

    # Loome graafikud kasutades PyQtGraph'i
    # Rohkem informatiooni leiab uurides dokumentatsiooni https://pyqtgraph.readthedocs.io/en/latest/plotting.html
    # ning muidugi otsides näiteid internetist https://pyqtgraph.readthedocs.io/en/latest/introduction.html#examples
    win = pg.GraphicsLayoutWidget(show=True, title="Pendlite positsioon ajas")

    # Loome esimese graafiku (pendel1) kasutades kosinust
    p1 = win.addPlot(x=t, y=pendulum1, title="<span style='font-size: 20pt;'>(COS) - Pendli positsioon ajas</span>")
    p1.addLegend() # Lisame legendi
    p1.plot(name="<span style='font-size: 20pt;'>Funktsioon(COS): 5 * cos(t)</span>", size='20pt')
    p1.setLabel("left", "pendel1", units="cm") # Märgistame vasaku telje
    p1.setLabel("bottom", "aeg", units="min") # Märgistame alumise telje
    p1.showGrid(x=True, y=True) # Kuvame ruudustiku
    p1.setXRange(0, 6.28) # Seame X-telje ulatuse
    p1.addLine(x=6.28, pen="g") # Lisame vertikaalse joone
    win.nextRow()

    p2 = win.addPlot(x=t, y=pendulum2, title="<span style='font-size: 20pt;'>(SIN) - Pendli positsioon ajas</span>")
    p2.addLegend()
    p2.plot(x=t, y=pendulum2, name="<span style='font-size: 20pt;'>Funktsioon(SIN): 5 * np.sin(t - np.pi/2)</span>", pen=(255, 0, 0))
    p2.setLabel("left", "pendel2", units="cm")
    p2.setLabel("bottom", "aeg", units="min")
    p2.showGrid(x=True, y=True)
    p2.setXRange(0, 6.28)
    p2.addLine(x=6.28, pen="y")
    win.nextRow()

    p3 = win.addPlot(X=t, title="<span style='font-size: 20pt;'>Kahe pendli positsioon ajas(sin/cos)</span>")
    p3.addLegend()
    p3.setLabel("left", "pendel1/2", units="cm")
    p3.setLabel("bottom", "aeg", units="min")
    p3.showGrid(x=True, y=True)
    p3.setXRange(0, 6.28)
    p3.addLine(x=6.28, pen="b")
    p3.addLegend()
    p3.plot(x=t, y=pendulum1, name="<span style='font-size: 20pt;'>Funktsioon(COS): 5 * cos(t)</span>")
    p3.plot(x=t, y=pendulum2, pen=(255, 0, 0), name="<span style='font-size: 20pt;'>Funktsioon(SIN): 5 * np.sin(t - np.pi/2)</span>") # Joonistame teise graafiku

    # Alustame GUI peatsükliga, blokeeruv
    QtWidgets.QApplication.instance().exec_()


data_line = None
data = []

##ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
aeg_lopp = time.time() + 31
salvestatud = False

def on_update():
    global data_line, data, ser, salvestatud
    # Implementeerige siia andmete kuvamise loogika
    #data_line.setData(np.random.normal(size=500, loc=2.5))
    data += read_data_from_serial(ser)

    # Uuendab graafikut viimaste 500 andmepunktidega
    data_line.setData(data[-500:])
     # Kontrollib, kas määratud aeg on möödunud ja andmed pole veel salvestatud
    if time.time() > aeg_lopp and not salvestatud:
        salvestatud = True # Märgib, et andmed on salvestatud
        # Salvestab andmed faili
        np.save("andmed/numpy/p01_yl5_andmed.npy", data)
        print("salvestatud")
        print("kohe loen koodi")
        # Loeb salvestatud andmed failist
        lugemine = np.load("andmed/numpy/p01_yl5_andmed.npy")
        print(lugemine)
        pass


def yl5():
    global data_line, ser
    win = pg.GraphicsLayoutWidget(show=True, title="Real time data plotting")

    start_x = 0
    start_y = 0
    view_width = 500
    view_height = 5
    data_plot = win.addPlot()
    data_plot.setLabel("left", "Pinge", units ="v")
    data_plot.setLabel("bottom", "500 viimast andmepunkti")
    data_plot.setRange(QtCore.QRectF(start_x, start_y, view_width, view_height))
    data_line = data_plot.plot(pen='y')

    # Loob taimeri, mis kutsub välja funktsiooni on_update() 100 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update)
    timer.start(10)
    QtWidgets.QApplication.instance().exec_()


def yl3_kodutoo_morse():

    # antud signaal
    #signal = [5, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.024437927663734114, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.04398826979472141, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.04398826979472141, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.039100684261974585, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.039100684261974585, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 0.039100684261974585, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.039100684261974585, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.039100684261974585, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 5, 5, 5, 5, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.024437927663734114, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.04398826979472141, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.04398826979472141, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.039100684261974585, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.039100684261974585, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.039100684261974585, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.039100684261974585, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.039100684261974585, 0.034213098729227766, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 5, 5, 5, 5, 0.034213098729227766, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 0.034213098729227766, 0.02932551319648094, 0.02932551319648094, 0.034213098729227766, 5, 5, 5, 5, 0.034213098729227766, 0.02932551319648094]

    signal_path = r"C:/Users/ralfs/dsp-loti.05.064-ralf-suss-b31108-23-24k/praktikumid/andmed/numpy/p01_yl5_andmed.npy"
    signal = np.load(signal_path)

    # Teisendame signaali binaarseks jadaks
    binary_signal = [1 if x == 5 else 0 for x in signal]

    # Loome ajatelje signaali visualiseerimiseks
    t = np.arange(len(binary_signal)) # t on sama pikk kui binary_signal
    t = np.append(t, t[-1] + 1)  # Lisame t-le ühe elemendi, et see oleks binary_signal'ist ühe võrra pikem

    app = QtWidgets.QApplication(sys.argv)

    # Muudan kogu rakenduse teksti suurust
    font = QFont()
    font.setPointSize(20)  # Teen teksti suuremaks
    app.setFont(font)

    # Graafiku akna loomine
    win = pg.GraphicsLayoutWidget(show=True, title="Binaarse Signaali Visualiseerimine")
    win.resize(1000, 200)
    plot = win.addPlot(title="<span style='font-size: 20pt;'>Binaarne Signaal")
    plot.plot(t, binary_signal, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))

    # Alustame GUI peatsükliga, blokeeruv
    app.exec_()




def main():
    #yl2()
    #yl3()
    #yl3_filtering_with_masks()
    yl4()
    #yl5()
    #yl3_kodutoo_morse()


if __name__ == "__main__":
    main()



