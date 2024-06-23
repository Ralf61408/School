#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def convolve_impulse(amplitude, time_index, imp_response, length):
    """
    Funktsioon, mis täidab ühe alamosa konvolutsiooni sisendsignaali algoritmist
    (arvutab tulemuse sisendsignaali ühe sämpli jaoks).

    Sisendid:
    amplitude - vaatluse all oleva sisendsignaali sämpli väärtus (impulsi [0, 0, -3] puhul -3)
    time_index - vaatluse all oleva sisendsignaali sämpli esinemise ajahetk ((impulsi [0, 0, -3] puhul 2))
    imp_response - signaal, millega konvoleeritakse (nt [0.5, 1, -2])
    length - tulemuseks oleva massiivi/järjendi pikkus (peab olema piisav, et tulemus mahuks ära, võib olla pikem)

    Tagastab:
    result - Massiiv/järjend pikkusega 'length', milles on alates indeksist 'time_index' väärtused 'imp_response' sisendist,
        mis on 'amplitude' väärtusega läbi korrutatud. Ülejäänud väärtused on nullid.
    """
    result = np.zeros(length)

    for impulsskoste_1_v22rtus in imp_response:
        
        result[time_index] = amplitude * impulsskoste_1_v22rtus

        time_index += 1
        
    return result


def convolve_1d(input_signal, imp_response):
    """
    Funktsioon ise kirjutatud konvolutsiooni teostamiseks sisendsignaali algoritmi kaudu.
    Konvolutsiooni teostamiseks peab kasutama eelnevalt loodud abifunktsiooni.

    Sisendid:
    input_signal - konvolutsiooni esimene sisendsignaal
    imp_response - signaal, millega esimest signaali konvoleeritakse

    Tagastab:
    result - Massiiv/järjend sobiva pikkusega, milles on kahe sisendiks oleva signaali konvolutsiooni tulemus.

    Ralf:Numpy kasutab FFT-d, numpy teek kasutab tõhusamalt protsessori vektorarvutust. NumPy teek oskab paremini kasutada mälu.
    """

    aja_indeks = 0

    pikkus = len(input_signal) + len(imp_response) - 1
    result = np.zeros(pikkus)

    for impulsskoste_1_v22rtus in input_signal:
        result += convolve_impulse(impulsskoste_1_v22rtus, aja_indeks, imp_response, pikkus)
        aja_indeks += 1

    return result


def convolve_2d(input_signal, kernel):
    """
    Funktsioon ise kirjutatud konvolutsiooni teostamiseks kahemõõtmelistele sisendsignaalidele väljundsignaali algoritmi kaudu.

    Sisendid:
    input_signal - kahemõõtmeline sisendsignaal
    kernel - kahemõõtmeline signaal, millega esimest signaali konvoleeritakse (kernel)

    Tagastab:
    result - Kahemõõtmeline massiiv, milles on kahe sisendiks oleva signaali konvolutsiooni tulemus.
    """
    # flipime 90kraadi(read) ja siis fliplr nihutame
    kernel = np.flipud(np.fliplr(kernel))
    #print("Pärast kernel: ", kernel)
    x_input = len(kernel[0])//2
    #print(x_input)
    y_input = len(kernel)//2
    #print(y_input)

    result = np.zeros_like(input_signal)
    #print("see on signaal pilt:", input_signal)

    input_signal_padded = np.zeros((input_signal.shape[0] + y_input*2, input_signal.shape[1] + x_input*2))
    # liidame pikkusele ja laiusele 2 juurde, saame 0 2d mõõtmelise massiivi ja et tekiks ümberringi nullid. pildi ümber luuakse regioon väärtusega 0

    #print("input_signal_padded: ", input_signal_padded)

    input_signal_padded[y_input:-abs(y_input), x_input:-abs(x_input)] = input_signal
    #print("uus signaal padded: ", input_signal_padded)
    #mahutasime pildi regiooni 0-lide sisse, indekseerimise operation

    x_input = len(kernel[0])
    #print("minu x input: ", x_input)
    y_input = len(kernel)
    #print("minu y input: ", y_input)
    #print("minu input: ", input_signal)

    for x in range(input_signal.shape[1]):
        for y in range(input_signal.shape[0]):
            # Käin elementhaaval läbi, teen input signal padded-ist kastikese mille korrutan kerneli elemnthaaval läbi ja lõpuks liidan kokku
            result[y, x] = (kernel * input_signal_padded[y: y+y_input, x: x+x_input]).sum()
            #print("Minu vastus: ", result)
    return result
