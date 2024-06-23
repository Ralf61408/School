#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyvisa, serial
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
from abi.visual.plot_stem import simple_plot_stem
from dst.device.decode_preamble import convert_waveform_preamble, create_x_axis_values, convert_data_to_volts
from dst.device.read_from_arduino import read_data_from_serial
from dst.math.impulse import ühikimpulsi_loomine



yl3_data_line = None
instrument_osc = None
#ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
data_line = []
data = []

def on_update():
    global data_line, data, ser
    # Implementeerige siia andmete kuvamise loogika
    ##new_data = read_data_from_serial(ser)
    new_data = read_data_from_serial(ser)
    data.extend(new_data)
    if len(data) > 500:
        data = data[-500:]  # Piiran andmete hulka viimase 500 punktiga
    step = 0.005  # Ajavahemik mõõtmiste vahel sekundites
    x = np.linspace(-len(data) * step, 0, len(data))
    data_line.setData(x=x, y=data)



def yl1():
    global data_line, ser
    win = pg.GraphicsLayoutWidget(show=True, title="Real time data plotting")
    start_x = 0
    start_y = 0
    view_width = 500*0.005
    view_height = 5
    data_plot = win.addPlot()
    data_plot.setLabel("left", "Pinge", units ="V")
    data_plot.setLabel("bottom", "Aeg", units = "s")
    #data_plot.setRange(QtCore.QRectF(start_x, start_y, view_width, view_height))
    data_line = data_plot.plot(pen='y')

    # 50 millisekundiga korrutama ja mappima
    # Loob taimeri, mis kutsub välja funktsiooni on_update() 100 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update)
    timer.start(1000)
    QtWidgets.QApplication.instance().exec_()


def yl3():
    global yl3_data_line, instrument_osc
    rm = pyvisa.ResourceManager()
    # NB! Sisesta oma ostsilloskoobi IP!
    instrument_osc = rm.open_resource('TCPIP::172.17.55.132::INSTR', read_termination="\n", write_termination="\n")

    instrument_osc.write('WAV:SOUR CHAN2') # Valime kanali andmepunktide salvestamiseks
    instrument_osc.write(':WAV:MODE NORM') # Loeme ainult andmed, mis on ekraanil (Ekraanile mahub 1200 punkti)
    instrument_osc.write(':WAV:FORM BYTE') # Üks sisendsignaali punkt mahub ühte baiti kuna DS1054Z on 8-bitine ostsilloskoop
    instrument_osc.write(':WAV:START 1')   # Salvestatud signaali esimene punkt, mida lugeda
    instrument_osc.write(':WAV:STOP 1200') # Salvestatud signaali viimane punkt, mida lugeda

    # Küsime mõõteriistalt IEEE standardile vastava andmeploki
    waveform_datapoints = instrument_osc.query_binary_values(':WAV:DATA?', datatype="B", container=np.array).astype(np.float32)

    # Küsime mõõteriistalt mõõtmisel kasutatud parameetrid ja teisendame need lihtsasti kasutavaks sõnastikuks
    preamble_dict = convert_waveform_preamble(instrument_osc.query(":WAVEFORM:PREAMBLE?"))

    x = create_x_axis_values(preamble_dict)
    
    y = convert_data_to_volts(waveform_datapoints, preamble_dict)

    # Loome graafilise akna, et kujutada saadud informatsiooni
    win = pg.GraphicsLayoutWidget(show=True, title="Ostsilloskoobi andmed")
    data_plot = win.addPlot()

    yl3_data_line = data_plot.plot(pen='y')
    yl3_data_line.setData(x=x, y=y)
    data_plot.setLabel("left", "pinge", units="v")
    data_plot.setLabel("bottom", "aeg (s)")

    # Loob taimeri, mis kutsub välja funktsiooni on_update() 100 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update)
    timer.start(10)
    # Alustame GUI peatsükliga, blokeeruv
    QtWidgets.QApplication.instance().exec_()

    # Sulgeme ühenduse mõõteriistaga
    instrument_osc.close()

def yl5():
    # Juhuslike arvude generaator, mille abil luuakse näidisgraafikutele kuvatavad signaalid
    rng = np.random.default_rng()
    win = pg.GraphicsLayoutWidget(show=True, title="Impulsside summa")
    list = []

    impulss = ühikimpulsi_loomine(5, 0, 3)
    list.append(impulss)
    p1 = win.addPlot()
    simple_plot_stem(p1, impulss)
    p1.setLabel('top', 'impulss 1')

    impulss2 = ühikimpulsi_loomine(5, 3, -3)
    list.append(impulss2)
    p2 = win.addPlot()
    simple_plot_stem(p2, impulss2)
    p2.setLabel("top", "impulss 2")

    impulss3 = ühikimpulsi_loomine(5, -2, 2)
    list.append(impulss3)
    p3 = win.addPlot()
    simple_plot_stem(p3, impulss3)
    p3.setLabel("top", "impulss 3")
    win.nextRow()

    impulss4 = ühikimpulsi_loomine(5, -1, 1)
    list.append(impulss4)
    p4 = win.addPlot()
    simple_plot_stem(p4, impulss4)
    p4.setLabel("top", "impulss 4")

    impulss5 = ühikimpulsi_loomine(5, -2, 1)
    list.append(impulss5)
    p5 = win.addPlot()
    simple_plot_stem(p5, impulss5)
    p5.setLabel("top", "impulss 5")

    impulss6 = ühikimpulsi_loomine(5, 3, -2)
    list.append(impulss6)
    p6 = win.addPlot()
    simple_plot_stem(p6, impulss6)
    p6.setLabel("top", "impulss 6")

    win.nextRow()

    impulss_kokku = sum(list)
    print("a", impulss_kokku)
    p7 = win.addPlot(colspan=3)
    simple_plot_stem(p7, impulss_kokku)
    p7.setLabel('top', 'terve signaal')

    QtWidgets.QApplication.instance().exec_()

def yl6():
    #rng = np.random.default_rng()
    win = pg.GraphicsLayoutWidget(show=True, title="Impulsside summa")
    list = []
    a = 0
    amplituud = 0


    while a < 73: # Tsükkel, mis töötab kuni 73 impulssi on loodud
        impulss = ühikimpulsi_loomine(73, -a, np.sin(amplituud)) # Loob ühikimpulsi pikkusega 73, nihkega -a ja amplituudiga sin(amplituud)
        amplituud += 10 * np.pi/180 # Suurendab amplituudi väärtust 10 kraadi võrra (radiaanides)
        list.append(impulss) # Lisab loodud impulssi listi
        #p1 = win.addPlot()
        #simple_plot_stem(p1, impulss)
        #p1.setLabel('top', 'impulss 1')
        a += 1 # Suurendab loendurit, et liikuda järgmise impulsi juurde
    impulss_kokku = sum(list) # Summeerib kõik loodud impulsid
    p7 = win.addPlot(colspan=1)
    simple_plot_stem(p7, impulss_kokku)
    p7.setLabel('top', 'terve signaal')

    p8 = win.addPlot(colspan=1)
    simple_plot_stem(p8, list[50])
    p8.setLabel('top', 'Üks Signaal')

    QtWidgets.QApplication.instance().exec_()


def main():
    #yl1()
    #yl3()
    #yl5()
    yl6()

if __name__ == "__main__":
    main()