import os  # Import os moodulist, mis võimaldab töödelda failisüsteemi operatsioone
import numpy as np  # Import NumPy teegist, mis on vajalik numbriliste arvutuste jaoks
import pyqtgraph as pg  # Import pyqtgraph teegist, mis on vajalik graafikute kuvamiseks
from pyqtgraph.Qt import QtWidgets, QtCore  # Import QtWidgets ja QtCore PyQtGraphi Qt moodulist
from scipy.io import wavfile  # Import scipy.io teegist, mis võimaldab heliandmete lugemist ja salvestamist
import serial  # Import pySerial teegist, mis on vajalik seriaalühenduse jaoks
import time  # Import time teegist, mis on vajalik ajamõõtmiseks ja viivituste tegemiseks
import pyvisa

from dst.device.connect_to_power_supply import power_supply_get_instrument  # Import funktsioonist toiteploki ühendamiseks
from dst.device.read_from_oscilloscope import get_oscilloscope_data  # Import funktsioonist andmete lugemiseks ostsilloskoobist
from dst.device.decode_preamble import create_x_axis_values, convert_data_to_volts  # Import funktsioonidest andmete teisendamiseks ja x-telje väärtuste loomiseks
from dst.device.read_from_arduino import read_data_from_serial  # Import funktsioonist andmete lugemiseks seriaalühendusest Arduino kaudu

# Funktsioon ühe signaali genereerimiseks
def generate_single_signal(inst: pyvisa.resources.Resource, frequency: float):
    """
    Funktsioon, mis seadistab sisendina antud seadme genereerima sinusoidi signaali määratud sagedusega.
    Signaal genereeritakse 2. kanalile.
    Sisendid:
        inst - PyVISA signaaligeneraatori ressursi objekt. Tüüp: pyvisa.resources.Resource.
        frequency - Sinusoidi sagedus hertsides
    """
    inst.write(":SYSTem:CHANnel:CURrent CH2")
    inst.write(f":SOURce2:APPLy:SINusoid {frequency}Hz,5Vpp")
    inst.write(":OUTPut2 ON")

# Funktsioon ostsilloskoobilt andmete lugemiseks
def read_oscilloscope_data():
    waveform_datapoints, preamble_dict = get_oscilloscope_data('172.17.55.20', 1, 0.3, -1.25)  # Loeb andmed ostsilloskoobist, kasutades imporditud funktsiooni

    x = create_x_axis_values(preamble_dict)  # Loob x-telje väärtused graafiku jaoks, kasutades imporditud funktsiooni
    y = convert_data_to_volts(waveform_datapoints, preamble_dict)  # Teisendab ostsilloskoobi andmed voltideks, kasutades imporditud funktsiooni

    return x, y, preamble_dict

# Funktsioon toiteploki seadistamiseks
def setup_power_supply():
    toide = power_supply_get_instrument()  # Loob ühenduse toiteplokiga, kasutades imporditud funktsiooni
    toide.write(':OUTP CH1,ON')  # Lülitab sisse esimese kanali toiteplokil
    toide.write(':SOURce1:VOLTage 5')  # Seadistab esimese kanali pinge 5V
    toide.write(':SOURce1:CURRent 0.05')  # Seadistab esimese kanali voolu 0.05A
    return toide

# Funktsioon graafiku uuendamiseks
def update_plot():
    global data_line, data, ser, salvestatud, data2, MA_result, spectrum_plot
    arduino = read_data_from_serial(ser)
    
    # Andmete töötlemine ja teisendamine
    sisendandmed = [a / 1023 * 4 for a in arduino]
    data += sisendandmed

    if len(data) > 500:
        data = data[-500:]  # Piiran andmete hulka viimase 500 punktiga
    
    # Eemaldab DC-offseti
    centered_data = data - np.mean(data)
    
    # Rakendab Hanningi akent
    hanning_window = np.hanning(len(centered_data))
    windowed_data = centered_data * hanning_window
    
    # Fourier' teisendus
    fft_result = np.fft.fft(windowed_data)
    fft_magnitude = np.abs(fft_result) / len(fft_result)
    
    # Sagedustelgede loomine
    freq_axis = np.linspace(0, 2000, len(fft_magnitude))
    
    # Uuendab graafikut reaalajas
    data_line.setData(data)
    
    # Kuvab sagedusspektri
    spectrum_plot.setData(freq_axis, fft_magnitude[:len(freq_axis)])
    
    # Seadistab taimeri, et uuendada graafikut iga 5 ms järel
    QtCore.QTimer.singleShot(5, update_plot)

# Põhifunktsioon
def main():
    global curve, data_buffer, ptr, serial_connection, data_line, data, salvestatud, data2, MA_result, spectrum_plot  # Global muutujad, mida kasutatakse graafiku uuendamisel

    serial_connection = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)  # Loob seriaalühenduse määratud porti ja baudi kiirusega
    data_buffer = np.zeros(2000)  # Loob andmepuhvri suurusega 2000, et mahutada 2 kHz sämplimissagedust
    data = []
    data2 = []
    salvestatud = False

    sampling_rate = 2000  # Määrab Arduino sämplimissageduse otse 2 kHz
    print(f"Sampling rate: {sampling_rate} samples per second")  # Prindib sämplimissageduse

    app = QtWidgets.QApplication([])  # Loob Qt rakenduse
    win = pg.GraphicsLayoutWidget(show=True, title="Realtime Data")  # Loob graafiku akna
    plot = win.addPlot(title="Reaalajas andmed")  # Lisab graafiku aknasse
    data_line = plot.plot(pen='y')  # Loob graafiku kõvera

    # Kuvab sagedusspektri
    spectrum_plot = win.addPlot(title="Sagedusspekter")  # Loob sagedusspektri graafiku akna
    spectrum_plot.setLabel('left', 'Amplituud')
    spectrum_plot.setLabel('bottom', 'Sagedus', units='Hz')
    
    curve = plot.plot()  # Loob graafiku kõvera
    update_plot()  # Käivitab graafiku uuendamise funktsiooni

    # Seadistab toiteploki
    toide = setup_power_supply()

    # Genereerib 4 kHz signaali
    instrument = power_supply_get_instrument()  # Loob ühenduse signaaligeneraatoriga
    generate_single_signal(instrument, 4000)  # Genereerib 4 kHz signaali

    # Loeb andmed ostsilloskoobist
    x, y, preamble_dict = read_oscilloscope_data()

    # Kuvab ostsilloskoobist saadud andmed
    win2 = pg.GraphicsLayoutWidget(show=True, title="Oscilloscope Data")
    plot2 = win2.addPlot(title="Mõõdetud pinge")
    plot2.setLabel('left', 'Pinge', units='V')
    plot2.setLabel('bottom', 'Aeg', units='s')
    plot2.plot(x, y)
    
    # Sulgeb toiteploki ühenduse
    toide.write(':OUTPut CH1,OFF')
    toide.close()

    sample_rate = 1 / (preamble_dict['x_increment'])  # Arvutab sämplimissageduse ostsilloskoobi andmete põhjal
    data_norm = y - np.mean(y)  # Nulli ümber tsentreerimine
    data_norm /= np.max(np.abs(data_norm))  # Normaliseerimine
    wavfile.write('andmed/audio/p08_yl3_in.wav', int(sample_rate), data_norm)  # Salvestab normaliseeritud andmed helifailina

    QtWidgets.QApplication.instance().exec_()  # Käivitab Qt rakenduse, et kuvada graafik

if __name__ == '__main__':
    main()  # Käivitab põhifunktsiooni, kui skript käivitatakse
