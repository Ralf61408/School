#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pyqtgraph as pg
from scipy.io import wavfile
from dst.filter.onedim.frequency import *
from dst.visual.plot_filters import *
from abi.visual.p08_tasks import *
import os
audio_path = os.path.join(os.path.dirname(__file__), "andmed/audio")
import pyvisa
from dst.device.read_from_oscilloscope import get_oscilloscope_data
from dst.device.decode_preamble import create_x_axis_values, convert_data_to_volts
from pyqtgraph.Qt import QtCore, QtWidgets
from dst.device.connect_to_power_supply import power_supply_get_instrument



def yl1():
    # Loome graafilise kasutajaliidese.
    # Käsuga luuakse aken liuguritega, mille liigutamisel kutsutakse välja teie loodud filtri loomise funktsioon
    # ja seejärel graafiku kuvamise funktsioon.
    # start() funktsioon blokeerub kuni akna sulgemiseni.
    task1_gui = Task1()
    task1_gui.start()

def yl2():
    # Seadistage toiteploki esimene kanal ja lülitage sisse.
    rm = pyvisa.ResourceManager()
    toide = power_supply_get_instrument()
    #toide = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C214004113::INSTR')
    toide.write(':OUTP CH1,ON')
    toide.write(':SOURce1:VOLTage 5')
    toide.write(':SOURce1:CURRent 0.05')

    # Kasutades oma ostsilloskoobiga mõõtmise funktsiooni, lugege sisse andmed ja teisendage voltideks.
    waveform_datapoints, preamble_dict = get_oscilloscope_data('172.17.55.20', 1, 0.3, -1.25)

    # Lülitage toiteploki esimene kanal välja ja sulgege ühendus seadmega.

    #toide = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C214004113::INSTR')
    toide.write(':OUTPut CH1,OFF')
    toide.close()

    # Kuvage saadud andmed kontrollimiseks graafikul.

    x = create_x_axis_values(preamble_dict)
    
    y = convert_data_to_volts(waveform_datapoints, preamble_dict)

    win = pg.GraphicsLayoutWidget(show=True, title="yl3")
    plot = win.addPlot(title="Mõõdetud pinge")
    plot.setLabel('left', 'Pinge', units='V')
    plot.setLabel('bottom', 'Aeg', units='s')
    plot.plot(x, y)
    QtWidgets.QApplication.instance().exec_()

    # Normaliseerige andmed ja salvestage korrektse sämplimissagedusega faili.
    sample_rate = 1 / (preamble_dict['x_increment'] )#* preamble_dict['nr_of_points'])
    data_norm = y - np.mean(y) # Nulli ümber tsentreerimine
    data_norm /= np.max(np.abs(data_norm))  # Normaliseerimine
    wavfile.write('andmed/audio/p08_yl3_in.wav', int(sample_rate), data_norm)
    pass

def yl3():
    # Lugege sisse eelmises ülesandes salvestatud helifail.
    sr, data_in = wavfile.read('andmed/audio/p08_yl3_in.wav')  # Eeldame, et fail on korrektselt määratud

    # Antud kasutajaliidese konstruktor võtab sisendiks filtreeritavad andmed.
    task3_gui = Task3(data_in, sr)
    task3_gui.start()

    # get_filtered_data võimaldab välja lugeda filtreeritud andmed.
    filtered_data = task3_gui.get_filtered_data()

    # Saadud andmed salvestage helifaili.
    wavfile.write('andmed/audio/p08_yl3_filtered.wav', sr, filtered_data)
    ##

def yl4():
    # Kasutajaliides töötab sarnaselt eelnevaga kuid madalpääsfiltri asemel kasutatakse kõrgpääsfiltri loomise funktsiooni.
    task4_gui = Task4()
    task4_gui.start()

def yl5():
    # Lisage vajalikud käsud sarnaselt kolmandale ülesandele.
    sr, data_in = wavfile.read('andmed/audio/p08_yl5_in.wav')

    task9_gui = Task5(data_in, sr)
    task9_gui.start()

    # get_filtered_data võimaldab välja lugeda filtreeritud andmed.
    filtered_data = task9_gui.get_filtered_data()

    # Saadud andmed salvestage helifaili.
    wavfile.write('andmed/audio/p08_yl5_filtered.wav', sr, filtered_data)


def yl6():
    task6_gui = Task6()
    task6_gui.start()

def yl7_1():
    # Sarnaselt teisele ülesandele, salvestage ostsilloskoobiga vajalikud andmed.
    # Seadistage toiteploki esimene kanal ja lülitage sisse.
    rm = pyvisa.ResourceManager()
    toide = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C214004113::INSTR')
    toide.write(':OUTP CH1,ON')
    toide.write(':SOURce1:VOLTage 5')
    toide.write(':SOURce1:CURRent 0.05')
    toide.close()

    
    # Kasutades oma ostsilloskoobiga mõõtmise funktsiooni, lugege sisse andmed ja teisendage voltideks.
    waveform_datapoints, preamble_dict = get_oscilloscope_data('172.17.55.20', 1, 0.5, -1)


    # Lülitage toiteploki esimene kanal välja ja sulgege ühendus seadmega.

    toide = rm.open_resource('USB0::0x1AB1::0x0E11::DP8C214004113::INSTR')
    toide.write(':OUTPut CH1,OFF')
    toide.close()

    # Kuvage saadud andmed kontrollimiseks graafikul.
    x = create_x_axis_values(preamble_dict)
    
    y = convert_data_to_volts(waveform_datapoints, preamble_dict)

    win = pg.GraphicsLayoutWidget(show=True, title="yl")
    plot = win.addPlot(title="Mõõdetud pinge")
    plot.setLabel('left', 'Pinge', units='V')
    plot.setLabel('bottom', 'Aeg', units='s')
    plot.plot(x, y)
    QtWidgets.QApplication.instance().exec_()

    

    # Normaliseerige andmed ja salvestage korrektse sämplimissagedusega faili.

    sample_rate = 1 / (preamble_dict['x_increment'] )#* preamble_dict['nr_of_points'])
    data_norm = y - np.mean(y) # Nulli ümber tsentreerimine
    data_norm /= np.max(np.abs(data_norm))  # Normaliseerimine
    wavfile.write('andmed/audio/p08_yl7_in.wav', int(sample_rate), data_norm)
    pass

def yl7_2():
    # Lisage vajalikud käsud helifailide haldamiseks.
    sr, data_in = wavfile.read('andmed/audio/p08_yl7_in.wav')

    task7_gui = Task7(data_in)
    task7_gui.start()

    filtered_data = task7_gui.get_filtered_data()

    # Saadud andmed salvestage helifaili.
    wavfile.write('andmed/audio/p08_yl7_filtered.wav', sr, filtered_data)

def yl8():
    task8_gui = Task8()
    task8_gui.start()


def yl9():
    # Helifaili lugemine
    sr, data_in = wavfile.read('andmed/audio/p08_yl9_in.wav')

    task9_gui = Task9(data_in, sr)
    task9_gui.start()

    # get_filtered_data võimaldab välja lugeda filtreeritud andmed.
    filtered_data = task9_gui.get_filtered_data()

    # Salvestame filtreeritud andmed uude faili
    wavfile.write('andmed/audio/p08_yl9_filtered.wav', sr, filtered_data)


def main():
    # yl1()
    # yl2()
    # yl3()
    # yl4()
     yl5()
    # yl6()
    # yl7_1()
    # yl7_2()
    # yl8()
    # yl9()

if __name__ == '__main__':
    main()
