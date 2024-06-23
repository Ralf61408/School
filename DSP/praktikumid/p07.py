#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import pyvisa
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow
from dst.device.decode_preamble import convert_waveform_preamble, create_x_axis_values, convert_data_to_volts
from dst.device.connect_to_signal_generator import signal_generator_get_instrument
from dst.math.window_function import hann_window_function
from dst.filter.onedim.average import SMA, ESMA, LWMA, EMA
from abi.visual.SliderPlot import SliderPlot
from abi.visual.MainWindow import MainWindow
from dst.device.read_from_arduino import read_data_from_serial
import serial, time, random



def generate_pulse_signal(inst: pyvisa.resources.Resource):
    """
    Funktsioon, mis seadistab sisendina antud seadme genereerima kastsignaali
    amplituudiga 5 V, sagedusega 18 kHz, täiteteguriga 20%, signaal genereeritakse 2. kanalile.
    Sisendid:
        inst - PyVISA signaaligeneraatori ressursi objekt. Tüüp: pyvisa.resources.Resource.
    """

    # Valime kanali, mida soovime seadistama hakata.
    # Käsud on siin toodud sellisel kujul nagu leiab dokumentatsioonist - proovige käsud dokumentatsioonist üles leida.
    # Suurte tähtedega kujutatud osa on piisav käsu toimimiseks. Väiketähtedega osa on valikuline ja on toodud loetavuse huvides.
    inst.write(":SYSTem:CHANnel:CURrent CH2")

    # Kõigepealt paneme generaatori õigesse režiimi :source:apply kategooria käsuga.
    # Selle käsuga saab anda põhiparameetrid vastavalt dokumentatsioonis toodule.
    # Parameetrite ühikute andmisel saab kasutada detsimaaleesliiteid (SI). Ühiku ära jätmisel kasutatakse dokumentatsioonis toodud vaikeühikut.
    # Soovi korral võib parameetrid ka vahele jätta, ka sellel juhul kasutatakse vaikeväärtust.
    # Antud näites on jäetud vahele offset parameeter, mis tähendab, et vertikaalnihe on 0 V.
    inst.write(":SOURce2:APPLy:PULSe 18kHz,5Vpp,,30deg")

    # Keerulisemate signaalide lisaparameetreid, mida ei saa kaasa anda :source:apply käskudega, saab muuta :source:function kategooria vastava režiimi käskudega.
    # Antud näites muudame sel viisil pulss-signaali täiteteguri 20% peale.
    inst.write(":SOURce2:FUNCtion:PULSe:DCYCle 20%")

    # Peale seda, kui kanal on seadistatud, lülitame sisse väljundi.
    # Signaaligeneraator jääb seejärel meie soovitud signaali genereerima.
    inst.write(":OUTPut2 ON")


def generate_dual_signal(inst: pyvisa.resources.Resource, f1, f2):
    """
    Funktsioon, mis seadistab sisendina antud seadme genereerima dualtone signaali komponentidega 4 kHz ja 14 kHz.
    Signaal genereeritakse 2. kanalile.
    Sisendid:
        inst - PyVISA signaaligeneraatori ressursi objekt. Tüüp: pyvisa.resources.Resource.
        f1 - Esimese sinusoidi sagedus
        f2 - Teise sinusoidi sagedus
    """
    # TODO
    # Kanal 2 seadistamine dualtone signaali genereerimiseks
    inst.write(":SOURce2:FUNCtion DUALTone")
    inst.write(":SOURce2:FUNCtion:DUALTone:FREQ1 "+str(f1)+"kHz")
    inst.write(":SOURce2:FUNCtion:DUALTone:FREQ2 "+str(f2)+"kHz")
    inst.write(":SOURce2:FUNCtion:DUALTone:AMPLitude 5VPP") # iga tooni amplituudi seadmine
    inst.write(":SOURce2:FUNCtion:DUALTone:OFFSet 0V") # iga tooni vertikaalse nihke seadmine
    inst.write(":OUTPut2 ON")
    pass


def moving_average(input_signal, MA):
    """
    Keskmistab ette antud signaali kasutades antud liikuva keskmise objekti.
    Sisendid:
        input_signal - Signaal, millele tuleb rakendada liikuvat keskmist
        MA - Liikuva keskmise objekt
    Tagastab:
        Signaal, millel on rakendatud liikuvat keskmist
    """
    MA_result = np.zeros_like(input_signal)
    for index, elem in enumerate(input_signal):
        MA_result[index] = MA.average(elem)
    return MA_result


def yl1_2():
    # Juhuslik andmestik, mille peal testida liikuvate keskmiste toimimist.
    input_signal = np.cumsum(np.random.uniform(low=-10.0, high=10.0, size=250))

    # Liikuvate keskmiste algsed akna suuruse ja alfa väärtused
    # TODO: Vali algsed keskmistamise slaiderite väärtused.
    SMA_window_size = 1
    ESMA_window_size = 1
    LWMA_window_size = 1
    EMA_alpha = 1

    # Loome iga filtri tüübi kohta ühe isendi.
    test_SMA = SMA(SMA_window_size)
    test_ESMA = ESMA(ESMA_window_size)
    test_LWMA = LWMA(LWMA_window_size)
    test_EMA = EMA(EMA_alpha)

    # Keskmistame oma andmed kasutades kõiki implementeeritud keskmise leidmise meetodeid
    SMA_result = moving_average(input_signal, test_SMA)
    ESMA_result = moving_average(input_signal, test_ESMA)
    LWMA_result = moving_average(input_signal, test_LWMA)
    EMA_result = moving_average(input_signal, test_EMA)

    app = QApplication(sys.argv)
    SCRIPT_PATH = os.path.dirname(__file__)
    with open(os.path.join(SCRIPT_PATH, "abi/visual/styles.qss")) as file:
        app.setStyleSheet(file.read())
    mw = MainWindow()

    # Tulemuste kuvamine graafikutel
    slider_plot = SliderPlot(mw.grid, 1, plot_title="Liikuvad keskmised")
    SMA_plot = slider_plot.plot.plot(SMA_result, name="SMA", pen=pg.mkPen('r', width=2))
    ESMA_plot = slider_plot.plot.plot(ESMA_result, name="ESMA", pen=pg.mkPen('b', width=2))
    LWMA_plot = slider_plot.plot.plot(LWMA_result, name="LWMA", pen=pg.mkPen('g', width=2))
    EMA_plot = slider_plot.plot.plot(EMA_result, name="EMA", pen=pg.mkPen('m', width=2))
    # TODO: Lisa siin ESMA, LWMA ja EMA keskmistamise tulemused samale graafikule. Vali joontele värvid nii, et need oleks eristatavad.

    slider_plot.plot.plot(input_signal, name="Original", pen=pg.mkPen('y'))

    # Liugurite lisamine graafikutele
    # TODO: Vali liuguritele mõistlikud maksimum akna suuruse väärtused, et oleks võimalik akna suurust muuta ja näha kuidas erinevad suurused tulemust muudavad.
    slider_plot.add_slider(start=1, stop=50, func=lambda slider_value: SMA_plot.setData(moving_average(input_signal, SMA(slider_value))), label_text="SMA akna suurus", start_value=SMA_window_size, scaler=1, tracking=True)
    # TODO: Lisa siin slider_plot külge liugurid ESMA ja LWMA akna suuruste muutmiseks ning EMA alfa väärtuse muutmiseks.
    slider_plot.add_slider(start=1, stop=50, func=lambda slider_value: ESMA_plot.setData(moving_average(input_signal, ESMA(slider_value))), label_text="ESMA akna suurus", start_value=ESMA_window_size, scaler=1, tracking=True)
    slider_plot.add_slider(start=1, stop=50, func=lambda slider_value: LWMA_plot.setData(moving_average(input_signal, LWMA(slider_value))), label_text="LWMA akna suurus", start_value=LWMA_window_size, scaler=1, tracking=True)
    slider_plot.add_slider(start=1, stop=100, func=lambda slider_value: EMA_plot.setData(moving_average(input_signal, EMA(slider_value / 100))), label_text="EMA alpha", start_value=int(EMA_alpha * 100), scaler=0.01, tracking=True)


    mw.showMaximized()
    sys.exit(app.exec_())


def yl3():
    # Juhuslikud sisendandmed.
    signal_in = np.random.uniform(low=-1.0, high=1.0, size=1000)

    # Loome liikuva keskmise sooritamise isendi.
    # TODO: Lisada vajalikud parameetrid vastavalt oma implementatsioonile.
    test_MA = ESMA(5)  # või SMA() LWMA() EMA()

    # Keskmistame oma sisendandmed.
    MA_result = moving_average(signal_in, test_MA)

    # TODO: Viige sagedusruumi nii algne kui keskmistatud signaal ja kuvage graafikutel kummagi signaali sagedusruumi punktid ja nende suhe.

    # Sagedusruumi teisendamine
    fft_in = np.fft.rfft(signal_in)
    fft_MA = np.fft.rfft(MA_result)

    # Sageduste arvutamine
    freqs = np.fft.rfftfreq(len(signal_in))

    # Võimenduse arvutamine
    H_f = np.abs(fft_MA) / np.abs(fft_in)

    # Rakenduse ja akna loomine
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle('Frequency Response and System Gain')
    win.resize(1000, 400)

    # Graafikute widgeti loomine
    pg.setConfigOption('background', 'k')
    pg.setConfigOption('foreground', 'w')
    cw = pg.GraphicsLayoutWidget(show=True, title="Frequency Analysis")

    # Esimene graafik: sagedusvastus
    p1 = cw.addPlot(title="Frequency Response")
    p1.plot(freqs, np.abs(fft_in), name='Original Signal', pen = 'w')
    p1.plot(freqs, np.abs(fft_MA), pen='r', name='Filtered Signal (ESMA)')
    p1.setLabel('left', 'Amplitude')
    p1.setLabel('bottom', 'Frequency', units='Hz')
    p1.addLegend()

    # Teksti lisamine graafikule1
    text1 = pg.TextItem("Original Signal", color='w', anchor=(0,0))
    text2 = pg.TextItem("Filtered Signal (ESMA)", color='r', anchor=(0,0))
    p1.addItem(text1)
    p1.addItem(text2)
    text1.setPos(freqs[len(freqs)//2], np.max(np.abs(fft_in)))
    text2.setPos(freqs[len(freqs)//2], np.max(np.abs(fft_MA)))

    # Teine graafik: süsteemi võimendus
    cw.nextRow()
    p2 = cw.addPlot(title="System Gain Across Frequencies")
    p2.plot(freqs, H_f, pen='g', name='System Gain $H[f]$')
    p2.setLabel('left', 'Gain')
    p2.setLabel('bottom', 'Frequency', units='Hz')
    p2.addLegend()

    # Teksti lisamine graafikule2
    text3 = pg.TextItem("System Gain $H[f]$", color='g', anchor=(0,0))
    p2.addItem(text3)
    text3.setPos(freqs[len(freqs)//2], np.max(H_f))

    # Akna näitamine
    win.setCentralWidget(cw)
    win.show()

    sys.exit(app.exec_())


data_line = None
MA_result = None
#data_line2 = None
data = []
ser = None
data2 = []

ser = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=1)
aeg_lopp = time.time()
salvestatud = False
test_MA = ESMA(100)


def on_update():
    global data_line, data, ser, salvestatud, data2, MA_result
    # Implementeerige siia andmete kuvamise loogika
    arduino = read_data_from_serial(ser)
    data += arduino
    #MA_result = np.zeros_like(data)
   # data2 += arduino
    

    for index, elem in enumerate(arduino):
        data2.append(test_MA.average(elem))
        #print("MARESULT", MA_result)
        

    #data_line2.setData(MA_result[-500])
    data_line.setData(data[-500:])
    MA_result.setData(data2[-500:])
    #print("data", data)

    pass

def yl4():
    # Siia implementeerida juba esimese praktikumi lahendus, mis võtab vastu informatsiooni
    # Arduinolt ning hiljem keskmistab saadud tulemuse.
    global data_line, ser, data2, MA_result
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
    MA_result = data_plot.plot(pen='r')
    #data_plot.plot(MA_result, pen=pg.mkPen('r'), name='Liikuva keskmise tulemus')

    

    # Loob taimeri, mis kutsub välja funktsiooni on_update() 100 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update)
    timer.start(10)
    QtWidgets.QApplication.instance().exec_()
    # Kuvada samal graafikul muutmata kujul nii sisendandmed kui ka keskmistatud andmed.
    pass


def yl5():
    sig_inst = signal_generator_get_instrument()

    f1 = 4  # 4 kHz
    f2 = 14 # 14 kHz

    # TODO: Kasutage vastavalt ülesandele õiget funktsiooni kutset.
    # generate_pulse_signal(sig_inst)  # Näide
    generate_dual_signal(sig_inst, f1, f2)

    # Sulgeme ühenduse generaatoriga, generaatori töö jätkub iseseisvalt.
    sig_inst.close()

yl6_data_line = None
yl5_data_line = None
yl71_data_line = None
yl7_data_line = None

def on_update2():
    global data_line, data, ser, yl6_data_line, yl5_data_line, yl7_data_line, yl71_data_line
    # Implementeerige siia andmete kuvamise loogika
    # Küsime mõõteriistalt IEEE standardile vastava andmeploki
    waveform_datapoints = inst.query_binary_values(':WAV:DATA?', datatype="B", container=np.array).astype(np.float32)

    # Küsime mõõteriistalt mõõtmisel kasutatud parameetrid ja teisendame need lihtsasti kasutavaks sõnastikuks
    preamble_dict = convert_waveform_preamble(inst.query(":WAVEFORM:PREAMBLE?"))
    # Loome x-telje väärtused ajateljel kuvamiseks.
    x = create_x_axis_values(preamble_dict)
    
    #yl7
    y = convert_data_to_volts(waveform_datapoints, preamble_dict)
    z = hann_window_function(len(waveform_datapoints))
    y2 = y * z

    yl5_data_line.setData(x=x, y=y)
    yl71_data_line.setData(x=x, y=y2)

    # Arvutame sample rate'i
    sample_rate = 1 / (preamble_dict['x_increment'] )#* preamble_dict['nr_of_points'])


    # Arvutame Fourier'i pöörde
    y_fft = np.fft.fft(y)
    freq = np.fft.fftfreq(len(y), d=preamble_dict['x_increment'])

    # Arvutame Fourier'i pöörde
    y_fft2 = np.fft.fft(y2)
    freq2 = np.fft.fftfreq(len(y2), d=preamble_dict['x_increment'])

    # Kuvame Fourier'i pöörde graafikul
    yl6_data_line.setData(x=freq, y=np.abs(y_fft))
    yl7_data_line.setData(x=freq2, y=np.abs(y_fft2))
    pass


def yl6():
    # TODO: Genereeri signaaligeneraatorile vastavad sagedused.
    #https://en.wikipedia.org/wiki/Spectral_leakage
    # jagub 5,15,20, põhimõtteliselt 1200 puntki, siis vaja et see jaguks ning iga 1200 punkti tagant hakkaks uus 1200 punkti.komponendid mahuksid täisarv korda perioodi vaadeldavasse mõõteaknasse.
    sig_inst = signal_generator_get_instrument()
    #generate_dual_signal(sig_inst, f1=5, f2=20)
    f1  = random.randint(1500, 9000)
    print(f1)
    f2  = random.randint(1500, 9000)
    print(f2)
    generate_dual_signal(sig_inst, f1/1000, f2/1000)
    sig_inst.close()
    
    global yl5_data_line, inst, yl6_data_line, yl7_data_line, yl71_data_line
    rm = pyvisa.ResourceManager()
    # NB! Sisesta oma ostsilloskoobi IP!
    inst = rm.open_resource('TCPIP::172.17.55.20::INSTR', read_termination="\n", write_termination="\n")

     # Seadistame ajalise lahutuse 500 us/div
    inst.write(':TIMebase:SCALe 0.0002')

    # Valime kanali 2 andmepunktide salvestamiseks
    inst.write('WAV:SOUR CHAN2')

    # Loeme ainult andmed, mis on ekraanil (Ekraanile mahub 1200 punkti)
    inst.write(':WAV:MODE NORM')

    # Üks sisendsignaali punkt mahub ühte baiti kuna DS1054Z on 8-bitine ostsilloskoop
    inst.write(':WAV:FORM BYTE')

    # Salvestatud signaali esimene punkt, mida lugeda
    inst.write(':WAV:START 1')

    # Salvestatud signaali viimane punkt, mida lugeda
    inst.write(':WAV:STOP 1200')

    # Määrame vertikaalallahutuse 5V ja kuvatava kanali CHAN2 ja määrame kanali prooviku režiimi ja signaali sünkroniseerimise meetodi
    inst.write(":CHANnel2:SCALe 1V")
    inst.write(":CHANnel2:DISPlay ON")
    inst.write(":CHANnel2:PROBe 1")
    inst.write(":TRIGger:EDGe:SOURce CHAN2")
    inst.write(":TRIGger:EDGe:MODE EDGE")
    inst.write(":TRIGger:EDGe:LEVEL 2.4V")


    # Loome graafilise akna, et kujutada saadud informatsiooni
    win = pg.GraphicsLayoutWidget(show=True, title="Ostsilloskoobi andmed")
    data_plot = win.addPlot()

    # Joonistame andmed graafikule
    yl5_data_line = data_plot.plot(pen='y')
    yl71_data_line = data_plot.plot(pen='r')

    # Seame graafiku teljed
    data_plot.setLabel("left", "pinge", units="v")
    data_plot.setLabel("bottom", "aeg", units="s")

    # Lisame teise graafiku
    fft_plot = win.addPlot(row=1, col=0)

    # Joonistame Fourier' pöörde graafikule
    yl6_data_line = fft_plot.plot(pen='y')
    yl7_data_line = fft_plot.plot(pen='r')

    # Seame graafiku teljed
    fft_plot.setLabel("left", "Magnituud")
    fft_plot.setLabel("bottom", "Sagedus", units="Hz")

    # Loob taimeri, mis kutsub välja funktsiooni on_update() 100 korda sekundis
    timer = QtCore.QTimer()
    timer.timeout.connect(on_update2)
    timer.start(10)
    QtWidgets.QApplication.instance().exec_()

    # Sulgeme ühenduse mõõteriistaga
    inst.close()
    

    # TODO: Võta ostsilloskoobist vastu mõõdetud signaal.
    pass


def main():
    # yl1_2()
     yl3()
    # yl4()
    # yl5()
    # yl6()


if __name__ == "__main__":
    main()
