#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import os
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from dst.math.roots_of_unity import roots_of_unity
from abi.visual.plot_stem import plot_stem
from andmed.varia.p06_sample_signals import fft_test_signal, overlap_add_test_input, overlap_add_test_result
from dst.fourier.convolution import convolve_1d_fd, overlap_add_section_lengths
from dst.fourier.fft import fft, ifft
from dst.fourier.overlapadd.OverlapAdd import OverlapAdd
import time
from scipy.io import wavfile
from dst.math.convolution import convolve_impulse, convolve_1d, convolve_2d


SCRIPT_PATH = os.path.dirname(__file__)


def yl1():
    # Oma kompleksjuurte loomise korrektsuse kontroll. Erinevuste korral lõpetatakse programmi töö 'AssertionError'iga:
    # Kontrollitakse kahe massiivi võrdsust, vead raporteeritakse elementhaaval.
    roots_4 = np.array([1.0000000e+00+0.0000000e+00j, 6.1232340e-17-1.0000000e+00j, -1.0000000e+00-1.2246468e-16j, -1.8369702e-16+1.0000000e+00j])
    roots_7 = np.array([1.+0.j, 0.6234898-0.78183148j, -0.22252093-0.97492791j, -0.90096887-0.43388374j, -0.90096887+0.43388374j, -0.22252093+0.97492791j, 0.6234898+0.78183148j])
    np.testing.assert_allclose(roots_of_unity(4), roots_4, rtol=1e-07)
    np.testing.assert_allclose(roots_of_unity(7), roots_7, rtol=1e-07)

    # Kui kõik kontrollid olid edukad, jõuame järgmise käsuni:
    print("Kõik 1. ülesande testid edukalt läbitud!")


def yl2():
    win = pg.GraphicsLayoutWidget(show=True, title="FFT ja IFFT")

    signal_plot = win.addPlot()
    signal_plot.setTitle("Esialgne signaal")

    # Kuvame esialgse signaali üksikuid impulsse esile toova graafikuna. #
    plot_stem(signal_plot, np.array(fft_test_signal))

    win.nextRow()

    minu_fft = fft(fft_test_signal)
    minu_fft2 = np.absolute(minu_fft) / len(fft_test_signal)
    minu_faas = np.angle(minu_fft)
    p2 = win.addPlot()
    p2.setTitle("Oma implementeeritud FTT")
    plot_stem(p2, minu_fft2, minu_faas)
    p2.addLegend()
    win.nextRow()
    
    p3 = win.addPlot()
    p3.setTitle("Numpy FTT")
    numpy_dft = np.fft.fft(fft_test_signal)
    numpy_dft2 = np.absolute(numpy_dft) / len(fft_test_signal)
    numpy_faas = np.angle(numpy_dft)
    plot_stem(p3, numpy_dft2, numpy_faas)
    win.nextRow()

    p4 = win.addPlot()
    p4.setTitle("Oma implementeeritud IFFT")
    minu_ifft = ifft(minu_fft)
    plot_stem(p4, np.array(minu_ifft))

    QtWidgets.QApplication.instance().exec_()


def convert_to_frequency_domain(data, extra_params):
    return fft(data)


def process(data, extra_params):
    return data


def convert_to_time_domain(data, extra_params):
    return ifft(data)


def yl3():
    # 3: Overlap add klassi implementeerimine ning kasutamine
    overlap_add = OverlapAdd(
        win_size=64,
        hop_size=32,
        output_size=len(overlap_add_test_input),
        convert_to_frequency_domain=convert_to_frequency_domain,
        process=process,
        convert_to_time_domain=convert_to_time_domain,
        extra_params={}
    )
    result = overlap_add.run(overlap_add_test_input)
    #print("111111",result)

    np.testing.assert_array_almost_equal(result, overlap_add_test_result, err_msg="3: Ositi liitmine peaks tagastama täpselt sama signaali")
    print("3: Ositi liitmine tagastab sama signaali :)")


def yl4():
    
    
    # 4.1: Ositi konvoleerimise jaoks olulised parameetrid
    result_length, intermediate_length, long_slice_length = overlap_add_section_lengths(30000, 510)
    assert result_length == 30509 and intermediate_length == 1024 and long_slice_length == 515, "4.1: Ositi konvoleerimise parameetrid on valed"
    print("4.1: Funktsioon overlap_add_section_lengths tagastab korrektsed parameetrid :)")
    
    
    # 4.2: Ositi konvoleerimine läbi sagedusruumis korrutamise
    test_long_1 = np.random.random_sample(size = 800)
    test_long_2 = np.random.random_sample(size = 57)

    overlap_add_result = convolve_1d_fd(test_long_1, test_long_2)
    np_convolution_result = np.convolve(test_long_1, test_long_2)
    print("minu tehtud kood", overlap_add_result)
    print("np.poolt tehtud", np_convolution_result)

    np.testing.assert_array_almost_equal(overlap_add_result, np_convolution_result, err_msg="4.2: Konvolutsiooni tulemused ei kattu")
    print("4.2: Funktsioonide convolve_1d_fd ja np.convolve tulemused kattuvad :)")

# Helifailide lugemise funktsioon
def loe_faili(path):
    samplerate, data = wavfile.read(path)
    return samplerate, data.astype(np.float32)

# Normaliseerimisfunktsioon
def normaliseeri(signaal):
    return np.int16(signaal / np.max(np.abs(signaal)) * 32767)

def yl5():
    sr, data_esimene = loe_faili("andmed/audio/p06_guitar_short_sparse.wav")
    _, data_teine = loe_faili("andmed/audio/p03_ir_wide_hall_sparse.wav")

    # Sagedusdomeeni konvolutsioon
    algus = time.time()
    tulemus_fft = convolve_1d_fd(data_esimene, data_teine)
    lopp = time.time()
    print("FFT konvolutsiooni aeg: ", lopp - algus)
    tulemus_fft_norm = normaliseeri(tulemus_fft)

    # Ajadomeeni konvolutsioon
    algus2 = time.time()
    tulemus_aeg = convolve_1d(data_esimene, data_teine)
    lopp2 = time.time()
    print("Aja konvolutsiooni aeg: ", lopp2 - algus2)
    tulemus_aeg_norm = normaliseeri(tulemus_aeg)

    # Tulemuste salvestamine
    wavfile.write("andmed/audio/p06_yl4_freq_conv.wav", 8000, tulemus_fft_norm)
    wavfile.write("andmed/audio/p06_yl4_input_side_conv.wav", 8000, tulemus_aeg_norm)


def yl6():
    win = pg.GraphicsLayoutWidget(show=True, title="Sagedusvahemikud")
    signaali_graafik = win.addPlot(row=0, col=0, title="Algne signaal")
    
    # Loome signaali
    fs = 44100
    t = np.arange(fs) / fs
    f1, f2 = 120, 125
    A1, A2 = 1, 1
    x = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t)
    
    # Kujutame signaali ajadomeenis
    signaali_graafik.plot(t, x, pen='w')
    signaali_graafik.setLabel('left', "Väärtus(V)")
    signaali_graafik.setLabel('bottom', "Aeg", units='s')
    
    # Erineva pikkusega lõikude sagedusdomeeni esitus
    lengths = [None, 20000, 9000, 3000]  # None tähendab täispikka signaali
    for i, length in enumerate(lengths):
        if length is not None:
            signal_section = x[:length] # Võtab signaali algusest lõigu, kui length ei ole None
        else:
            signal_section = x # Kui length on None, võtab kogu signaali
            length = fs  # Täispikk signaal
        
        X_section = np.fft.fft(signal_section)
        magnitudes = np.abs(X_section)/length # Arvutab sageduskomponentide magnituudid ja normaliseerib pikkusega
        phases = np.angle(X_section)
        freqs = np.fft.fftfreq(length, 1/fs) # Arvutab sagedused vastavalt FFT pikkusele ja sämplimissagedusele

        # Kujutame sagedusdomeeni
        sagedus_graafik = win.addPlot(row=i+1, col=0, title=f"Signaali sagedusesitus teisendatuna Hz {length} andmepunkti baasil")
        plot_stem(sagedus_graafik, magnitudes[:len(freqs)//2], phases[:len(freqs)//2], freqs[:len(freqs)//2])
        sagedus_graafik.setLabel('left', "Magnituud|V|")
        sagedus_graafik.setLabel('bottom', "Sagedusvahemikud (n)", units='Hz')
        sagedus_graafik.setXRange(0, 150)

    QtWidgets.QApplication.instance().exec_()

"""
DFT lühemate signaalilõikude korral lähedased sagedused segunevad ja nihkuvad
44100 punkti korral on lahutusvõime umbes 1 Hz, 20000 punkti korral umbes 2.2 Hz, 
9000 punkti korral umbes 4.9 Hz ja 3000 punkti korral umbes 14.7 Hz




"""

def katsetus():
    win = pg.GraphicsLayoutWidget(show=True, title="Sagedusvahemikud")
    signaali_graafik = win.addPlot(row=0, col=0, title="Algne signaal")
    
    # Loome signaali
    fs = 44100
    t = np.arange(fs) / fs
    f1, f2 = 120, 125
    A1, A2 = 1, 1
    x = A1 * np.sin(2 * np.pi * f1 * t) + A2 * np.sin(2 * np.pi * f2 * t)
    
    # Kujutame signaali ajadomeenis
    signaali_graafik.plot(t, x, pen='w')
    signaali_graafik.setLabel('left', "Väärtus(V)")
    signaali_graafik.setLabel('bottom', "Aeg", units='s')
    
    # Erineva pikkusega lõikude sagedusdomeeni esitus, lisades nullid lõppu
    lengths = [None, 20000, 9000, 3000]
    for i, length in enumerate(lengths):
        if length is not None:
            signal_section = np.pad(x[:length], (0, fs-length), 'constant', constant_values=(0))
        else:
            signal_section = x
            length = fs  # Täispikk signaal
        
        X_section = np.fft.fft(signal_section)
        magnitudes = np.abs(X_section)/fs  # Kasutan siin normaliseerimiseks fs, kuna pikkus on fs pärast nullide lisamist
        phases = np.angle(X_section)
        freqs = np.fft.fftfreq(fs, 1/fs)  # Kasutame fs, kuna zero-padding'uga on kõik lõigud fs pikkused

        # Kujutame sagedusdomeeni
        sagedus_graafik = win.addPlot(row=i+1, col=0, title=f"Signaali sagedusesitus teisendatuna Hz {length} andmepunkti baasil")
        plot_stem(sagedus_graafik, magnitudes[:fs//2], phases[:fs//2], freqs[:fs//2])
        sagedus_graafik.setLabel('left', "Magnituud|V|")
        sagedus_graafik.setLabel('bottom', "Sagedusvahemikud (n)", units='Hz')
        sagedus_graafik.setXRange(0, 150)

    QtWidgets.QApplication.instance().exec_()
def main():
    # yl1()
    # yl2()
    # yl3()
    # yl4()
    # yl5()
     yl6()
    #    katsetus()


if __name__ == "__main__":
    main()
