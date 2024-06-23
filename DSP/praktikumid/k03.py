#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################################################################################################
#                                                                                                 #
#                           NB! Lahenda järgnevad ülesanded eraldi harul.                         #
#                                                                                                 #
###################################################################################################
import numpy as np
from scipy import signal
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtGui
import sys, cv2
from dst.math.convolution import convolve_2d
from dst.filter.twodim.kernels import blur, detect_edge




def kodu_1():
    # Ajatelg
    t = np.linspace(-2, 2, 1000, endpoint=False)
    # Esimene kastsignaal 1 Hz
    kast1 = np.clip(signal.square(2 * np.pi * 1 * t), 0, None)
    # Teine kastsignaal 0.5 Hz
    kast2 = np.clip(signal.square(2 * np.pi * 0.5 * t), 0, None)
    # Konvolutsioon
    convolved_initial = np.convolve(kast1, kast2, mode='same') / len(kast1)
    # Sawtooth signaali loomine 1 Hz
    sawtooth_wave = signal.sawtooth(2 * np.pi * 1 * t)
    # Konvolutsioon konvolutsiooni ja sawtooth_wave vahel
    final_convolution = np.convolve(convolved_initial, sawtooth_wave, mode='same') / len(convolved_initial)
    
    # Graafiku ettevalmistamine
    app = QtWidgets.QApplication(sys.argv)
    # Muudan kogu rakenduse teksti suurust
    font = QtGui.QFont()
    font.setPointSize(20)  # Teen teksti suuremaks
    app.setFont(font)

    # Esimene aken: kastsignaalid ja nende konvolutsioon
    win1 = pg.GraphicsLayoutWidget(show=True, title="Kastsignaalid ja nende konvolutsioon")
    win1.resize(800, 600)
    p1 = win1.addPlot(title="<span style='font-size: 20pt;'>Esimene kastsignaal")
    p1.plot(t, kast1, pen='r')
    p1.showGrid(x=True, y=True)
    win1.nextRow()
    p2 = win1.addPlot(title="<span style='font-size: 20pt;'>Teine kastsignaal")
    p2.plot(t, kast2, pen='g')
    p2.showGrid(x=True, y=True)
    win1.nextRow()
    p3 = win1.addPlot(title="<span style='font-size: 20pt;'>Konvolutsioon")
    p3.plot(t, convolved_initial, pen='b')
    p3.showGrid(x=True, y=True)

    """
    Kui mõlemate kastsignaalide väärtused on ühed, siis konvolutsiooni väärtus y teljel suureneb. Kui aga teise 
    kastsignaali väärtus y teljel muutus 0-liks, siis konvolutsiooni signaali y väärtus ei kasvanud enam 
    vaid liiklus horisontaalselt positiivse x telje suunas. Kui mõlema kastsignaali x ja y väärtused jõudsid 0 punkti, siis hakkab 
    vastupidine protsess vastavalt varasemalt kirjeldatule. Sellest 0 puntkist, kui mõlemate 
    kastsignaalide väärtused lähevad kõrgeks ehk üheks, siis konvolutsiooni y väärtus hakkab vähenema 
    niikaua kui mõlemate kastsignaalide väärtused on kõrged. 
    Lisaks: Kui üks signaalidest on null, siis loogiliselt kahe funktsiooni korrutamine ja nende 
    korrutiste summeerimine on null igal ajahetkel. Konvoltusiooni tulemus ei sõltu sellest punktist, 
    kuna iga korrutis, kus see punkt on kaasatud, on null. Seega hakkab konvolutsiooni horisontaalselt edasi liikuma, 
    sest osa sisendfunktsiooni väärtusest puudub matemaatilises tehtes.

    """

    # Teine aken: konvolutsioon ja sawtooth_wave ning nende konvolutsioon
    win2 = pg.GraphicsLayoutWidget(show=True, title="Konvolutsioon ja Sawtooth Wave")
    win2.resize(800, 600)
    p4 = win2.addPlot(title="<span style='font-size: 20pt;'>Konvolutsioon (kastsignaalid)")
    p4.plot(t, convolved_initial, pen='r')
    p4.showGrid(x=True, y=True)
    win2.nextRow()
    p5 = win2.addPlot(title="<span style='font-size: 20pt;'>Sawtooth Wave")
    p5.plot(t, sawtooth_wave, pen='g')
    p5.showGrid(x=True, y=True)
    win2.nextRow()
    p6 = win2.addPlot(title="<span style='font-size: 20pt;'>Lõplik Konvolutsioon")
    p6.plot(t, final_convolution, pen='b')
    p6.showGrid(x=True, y=True)

    """
   
    Näen, et "lõplik konvolutsioon" signaal on mõjutatud enamasti Sawtoothi signaalist:
    
    Kui X on negatiivne kõikide vaadeldavate graafikute puhul:

    Kui Sawtooth signaali väärtus on negatiivne(amplituud), siis "lõplik konvolutsioon" kahaneb ehk väärtus langeb.
    "Lõplik konvolutsioon" väärtus kahanes seni, kui Sawtooth signaal omas negatiivset väärtust.
    "Lõplik konvolutsioon" hakkas sujuvalt tõusma, kui sawtooth wave-i signaal omas positiivset y väärtust.

    Kui X on positiivne kõikide vaadeldavate graafikute puhul: Siis kõik on vastupidine, ehk Lõpliku konvolutsiooni väärtused on vastupidised.
    Kui (kastsignaalide) konvolutsioon ning Sawtooth signaali väärtused on mõlemad postiivsed(amplituud), siis hakkab "lõpliku konvolutsiooni" väärtus vaikselt langema. 
    
    Kui sawtooth signaali väärtus on negatiivne(amplituud), siis "lõpliku konvolutsiooni" väärtus tõuseb/suureneb 
    Kui kastsignaalide (konvolutsioon) väärtus ei suurenenud ning sawtoothi signaali väärtus y teljel oli positiivne, siis "lõplik konvolutsioon hakkas kahanema.
    "Lõplik konvolutsioon" kahanes seni, kui mõlemad (kastsignaalide) konvolutsioon ja Sawtooth signaal olid postiivsete väärtusega.

    """
    
    # Sündmuste tsükli käivitamine
    sys.exit(app.exec_())
   


def single_impulse_convolve(amplitude, time_index, imp_response, length):
    
    result = np.zeros(length)
    for impulsskoste_1_v22rtus in imp_response:

        result[time_index] = amplitude * impulsskoste_1_v22rtus

        time_index += 1

    return result


def input_side_convolution(in_sig, imp_response):
   
    aja_indeks = 0

    pikkus = len(in_sig) + len(imp_response) - 1
    result = np.zeros(pikkus)

    for impulsskoste_1_v22rtus in in_sig:
        result += single_impulse_convolve(impulsskoste_1_v22rtus, aja_indeks, imp_response, pikkus)
        aja_indeks += 1
        
    return result


def kodu_2():
    

    # Testsignaalid implementatsiooni katsetamiseks
    sig21 = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1])
    sig22 = np.array([-1, 1, -1, 0, 1, -1, 1])
    sig33 = np.array([-2, 1, 0, 0, 1, -1, 1])
    

    # Oma implementatsiooni võrdlemine NumPy konvolutsiooniga. Erinevuste korral lõpetatakse programmi töö 'AssertionError'iga:
    # kontrollitakse kahe massiivi võrdsust, vead raporteeritakse elementhaaval.
    """
    Kommutatiivsus: f * g = g * f"
    Konvolutsiooni kommutatiivsus tähendab, et kahe signaali konvolutsiooni tulemus on sama 
    sõltumata signaalide järjekorrast. See tähendab, et kui me konvoleerime kaks signaali: f signaal 
    signaaliga g ning siis konvoleerime vastupidi ehk konvoleerime signaal g signaaliga f, saame 
    sama tulemuse. Operandide järjekord ei mõjuta tulemit
    Matemaatiliselt võib seda väljendada kujul: f * g = g * f, kus “*” tähistab konvolutsiooni.

    """
    # konvulutsiooni kommutatiivsus
    np.testing.assert_array_equal(np.array(input_side_convolution(sig21, sig22)), np.convolve(sig22, sig21))
    
    print("Vahetasin signaalid omavahel ära(np.convolve), tulemuseks on sama vastus")
    # Operandide ehk signaalide järjekord ei mõjuta meie tulemit ehk tulemust - konvulutsiooni kommutatiivsus.
    
    
    # konvulutsiooni distributiivsus
    """
    Konvolutsiooni distributiivsus liitmise suhtes tähendab, et selle asemel konvolleerida signaali summa teise signaaliga, 
    võime selle asemel (sulud lahti teha) ning konvoleerida iga signaali paari eraldi ja siis summeerida tulemused. 
    Matemaatiliselt võib seda väljendada kujul: f * (g + h) = f * g + f * h, kus (f, g, h) on signaalid.
    """

    # Distributiivsuse demonstreerimine
    sig21_sig22sig33 = np.convolve(sig21, sig22 + sig33, mode='full')
    sig21sig22_sig21sig33 = np.convolve(sig21, sig22, mode='full') + np.convolve(sig21, sig33, mode='full')

    # Väljastame tulemused
    print("Konvolutsioon (f * (g + h)):", sig21_sig22sig33)
    print("Konvolutsioon ((f * g) + (f * h)):", sig21sig22_sig21sig33)

    np.testing.assert_array_equal(np.array(input_side_convolution(sig21, sig22 + sig33)), np.convolve(sig21, sig22) + np.convolve(sig21, sig33))
    print("Distributiivsus: f * (g + h) == f * g + f * h")
    print("konvulutsiooni Distributiivsus edukalt läbitud")

    # Kui kõik kontrollid olid edukad, jõuame programmi lõpuni:
    print("Kõik testid edukalt läbitud!")



def kodu_3():
    
    # Loeme pildi sisse ühe kanaliga (hallskaala pildina).
    # Saadav img muutuja on 2-mõõtmeline massiiv, millel saab rakendada
    # kõiki NumPy massiivi töötlemise võtteid.
    img = cv2.imread("andmed/images/numpy_logo.png", cv2.IMREAD_GRAYSCALE)
    Prewitt_x_edge_pilt = detect_edge(img, "Prewitt_x_edge")
    Prewitt_y_edge_pilt = detect_edge(img, "Prewitt_y_edge")
    
    # Kuvame tulemused
    # Loeme pildi sisse ühe kanaliga (hallskaala pildina).
    # Saadav img muutuja on 2-mõõtmeline massiiv, millel saab rakendada
    # kõiki NumPy massiivi töötlemise võtteid.    
    cv2.imshow('Originaalne pilt', img)
    cv2.imshow('Prewitt X', Prewitt_x_edge_pilt)
    cv2.imshow('Prewitt Y', Prewitt_y_edge_pilt)
    cv2.waitKey(0)  # Anname kontrolli OpenCV aknale. Programm blokeerub siin kuni klahvivajutuseni
    cv2.destroyAllWindows()


def main():
    kodu_1()
    kodu_2()
    kodu_3()

if __name__ == "__main__":
    main()
