#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2, time
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from scipy.io import wavfile
from dst.math.convolution import convolve_impulse, convolve_1d, convolve_2d
from dst.filter.twodim.kernels import blur, detect_edge


def measure_run_time(signal_in_1, signal_in_2):
    """
    Funktsioon, mis mõõdab samade sisenditega konvolutsioonile kuluvat aega nii 1. ülesandes
        implementeeritud lahenduse puhul kui ka NumPy optimiseeritud implementatsiooni puhul.

    Sisendid:
    signal_in_1 - üks konvolutsiooni sisendsignaalidest
    signal_in_2 - teine konvolutsiooni sisendsignaalidest (võib võtta kui impulsskostet)

    Tagastab:
    time_own - enda implementeeritud konvolutsiooni täitmisele kulunud aeg antud sisendsignaalide korral
    time_numpy - NumPy konvolutsiooni täitmisele kulunud aeg samade sisendsignaalide korral
    """

    # TODO Kirjuta lõpuni antud funktsioon
    time_own = time.time()
    convolve_1d(signal_in_1, signal_in_2)
    time_own_end = time.time() - time_own

    time_numpy = time.time()
    np.convolve(signal_in_1, signal_in_2)
    time_numpy_end = time.time() - time_numpy
    # Funktsioonide väljakutsed, mille ajakulu tuleb mõõta:
    # Ajakulu mõõtmiseks võib kasutada vabalt valitud vahendeid.

    return time_own_end, time_numpy_end


def yl1():
    # Testide plokk ülesande esimese poole (funktsiooni convolve_impulse) kontrollimiseks:
    # Omalt poolt võib kontrollimiseks lisada vahe- ja lõpptulemuste väljastamist ekraanile, kuvamist graafikul jms.

    # Testsignaalid implementatsiooni katsetamiseks:
    # Soovi korral võib sisendid konverteerida kohe NumPy massiivideks (np.array(minu_list)).
    sig11 = [0.5, 1, 2, 1, -1, -1]
    sig12 = [-1, 2, -1]

    # Oma implementatsiooni võrdlemine NumPy konvolutsiooniga. Erinevuste korral lõpetatakse programmi töö 'AssertionError'iga:
    # Kontrollitakse kahe massiivi võrdsust, vead raporteeritakse elementhaaval.
    np.testing.assert_array_equal(np.array(convolve_impulse(3, 2, sig11, 8)), np.convolve(sig11, [0, 0, 3]))
    np.testing.assert_array_equal(np.array(convolve_impulse(-2, 0, sig12, 3)), np.convolve(sig12, [-2]))
    np.testing.assert_array_equal(np.array(convolve_impulse(0.5, 3, sig12, 7)), np.convolve(sig12, [0, 0, 0, 0.5, 0]))

    # Kui kõik kontrollid olid edukad, jõuame järgmise käsuni:
    print("Kõik alamfunktsiooni testid edukalt läbitud!")

    # Testide plokk ülesande teise osa (funktsiooni convolve_1d) kontrollimiseks:

    # Testsignaalid implementatsiooni katsetamiseks
    sig21 = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    sig22 = [-1, 1, -1, 0, 1, -1, 1]
    sig23 = [4, 4, 4, 4, 3, 3, 3]
    sig24 = [2, 1, 3]

    # Oma implementatsiooni võrdlemine NumPy konvolutsiooniga. Erinevuste korral lõpetatakse programmi töö 'AssertionError'iga:
    # kontrollitakse kahe massiivi võrdsust, vead raporteeritakse elementhaaval.
    np.testing.assert_array_equal(np.array(convolve_1d(sig21, sig22)), np.convolve(sig21, sig22))
    np.testing.assert_array_equal(np.array(convolve_1d(sig22, sig23)), np.convolve(sig22, sig23))
    np.testing.assert_array_equal(np.array(convolve_1d(sig23, sig24)), np.convolve(sig23, sig24))
    np.testing.assert_array_equal(np.array(convolve_1d(sig24, sig21)), np.convolve(sig24, sig21))

    # Kui kõik kontrollid olid edukad, jõuame programmi lõpuni:
    print("Kõik testid edukalt läbitud!")


def yl2():
    # Testsignaalide loomine (iga järjendi element näitab, mitme elemendiga massiiv luuakse).
    # TODO Vali sobivad sisendsignaalide pikkused konvolutsiooni funktsioonide võrdlemiseks
    signal_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700]

    own_convolution_times = []
    numpy_convolution_times = []

    # Mõõdame ajad kõigi soovitud sisendi suuruste jaoks ja salvestame järjenditesse
    for size in signal_sizes:
        # Loome juhusliku sisendsignaali suurusega size ja teisendame selle loendiks
        signal1 = np.random.rand(size).tolist()  # Kasutame juhuslikke sisendeid valitud suurusega.
        signal2 = np.random.rand(size).tolist()

        time_own, time_numpy = measure_run_time(signal1, signal2)
        own_convolution_times.append(time_own)
        numpy_convolution_times.append(time_numpy)

    # Kuvame saadud ajad graafikul
    win = pg.GraphicsLayoutWidget(show=True, title="Efektiivsuse analüüs")

    p1 = win.addPlot(title = "Konvolutsiooni aja sõltuvus sisendi suurusest")
    p1.addLegend()
    p1.plot(signal_sizes, own_convolution_times, name="Oma implementatsioon", pen=(0,255,100))
    p1.plot(signal_sizes, numpy_convolution_times, name="NumPy implementatsioon", pen=(0,0,255))
    p1.setLabel(axis="left", text="Konvolutsioonile kulunud aeg", units="s")
    p1.setLabel(axis="bottom", text="Sisendsignaalide elementide arv")

    QtWidgets.QApplication.instance().exec_()


def yl3():
    samplerate_esimene, data_esimene = loefaili("/home/dsp-student03/dsp-loti.05.064-ralf-suss-b31108-23-24k/praktikumid/andmed/audio/p03_sample_violin.wav")
    print("a", samplerate_esimene, data_esimene)
    samplerate_teine, data_teine = loefaili("/home/dsp-student03/dsp-loti.05.064-ralf-suss-b31108-23-24k/praktikumid/andmed/audio/p03_ir_st_nicolas_church.wav")
    norm_esimene = normaliseering(data_esimene)
    norm_teine = normaliseering(data_teine)
    norm_lopp = normaliseering(np.convolve(norm_esimene, norm_teine))
    wavfile.write("/home/dsp-student03/dsp-loti.05.064-ralf-suss-b31108-23-24k/praktikumid/andmed/audio/p03_yl3_out.wav", samplerate_esimene, norm_lopp)

def normaliseering(data):

    max = None
    min = None

    for num_max in data:
        if (max is None or num_max > max):
            max = abs(num_max)
    print("Suurim v22rtus on: ", max)

    for num_min in data:
        if (min is None or num_min < min):
            min = abs(num_min)
    print("v2ikseim v22rtus on: ", min)

    if min < max:
        data = data/max
    else:
        data = data/min
    print("b", data)
    
    
    return data

def loefaili(path):
    samplerate, data = wavfile.read(path)
    return samplerate, data

def yl4():
    # Testsignaalide loomine:
    #input_signal = np.random.randint(0, 10, (8, 12))
    #kernel = np.random.randint(0, 10, (3, 3))

    input_signal = np.array((
    [ 1, 3, 3, 2, 6],
    [ 7, 9, 8, 9, 8],
    [ 7, 8, 6, 7, 4],
    [ 8, 9, 9, 7, 2]), dtype="int")

    kernel = np.array((
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1]), dtype="int")

    print(convolve_2d(input_signal, kernel))

    input_signal2 = np.array((
    [ 1, 3, 3, 2, 6, 6],
    [ 7, 9, 8, 9, 8, 4],
    [ 7, 8, 6, 7, 4, 2],
    [ 3, 2, 1, 5, 2, 3],
    [ 8, 9, 9, 7, 2, 8]), dtype="int")

    kernel2 = np.array((
    [-1, -2, -3, -2, -1],
    [ 0,  0,  0,  0,  0],
    [ 1,  2,  3,  2,  1]), dtype="int")

    print(convolve_2d(input_signal2, kernel2))


def yl5():
    # Loeme pildi sisse ühe kanaliga (hallskaala pildina).
    # Saadav img muutuja on 2-mõõtmeline massiiv, millel saab rakendada
    # kõiki NumPy massiivi töötlemise võtteid.
    img = cv2.imread("andmed/images/numpy_logo.png", cv2.IMREAD_GRAYSCALE)
    #img = (img / 2).astype(np.uint8)
    tulemus = blur(img, "box")
    tulemus1 = blur(img, "gaussian")
    tulemus2 = detect_edge(img, "sobel_x")
    tulemus3 = detect_edge(img, "sobel_y")
    tulemus4 = detect_edge(img, "laplacian")

    # Järgnevad käsud on vajalikud pildi kuvamiseks kasutades OpenCV teeki.
    #cv2.namedWindow("Input image", cv2.WINDOW_NORMAL)  # Loome akna, kuhu pildi kuvame
    cv2.imshow("Box Blur", tulemus)
    cv2.imshow("Gaussian Blur", tulemus1)
    cv2.imshow("Sobel X Edge", tulemus2)
    cv2.imshow("Sobel Y Edge", tulemus3)
    cv2.imshow("Laplacian Edge", tulemus4)  # Kuvame loodud aknas massiivi pildina
    cv2.waitKey(0)  # Anname kontrolli OpenCV aknale. Programm blokeerub siin kuni klahvivajutuseni
    cv2.destroyAllWindows()


def main():
    #yl1()
    #yl2()
    #yl3()
    yl4()
    #yl5()


if __name__ == "__main__":
    main()
